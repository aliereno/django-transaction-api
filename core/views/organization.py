from datetime import datetime, timedelta

import jwt
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from app.settings import JWT_EXPIRES_TIME, JWT_SECRET_KEY
from core.authentication import (
    OrganizationUserAuthentication,
    OrganizationUserPermissionCheck,
)
from core.models.enums.transaction import TransactionStatus, TransactionType
from core.models.organization import (
    Organization,
    OrganizationUser,
    OrganizationUserAuthHistory,
)
from core.models.transaction import Transaction, TransactionHandle
from core.serializers import (
    ApprovementRequest,
    AuthenticateSerializer,
    DepositWithdrawalRequest,
    TransactionResponse,
)
from core.tasks import handle_approved_transaction


class OrganizationDetailGenericView(APIView):
    def get_object(self, organization_id):
        try:
            obj = Organization.objects.get(pk=organization_id)
        except Organization.DoesNotExist:
            raise NotFound("Organization not found.")
        self.check_object_permissions(self.request, obj)
        return obj


class OrganizationAuthenticateView(OrganizationDetailGenericView):
    def post(self, request, organization_id=None):
        serializer = AuthenticateSerializer(data=request.data)
        serializer.is_valid(True)

        user = OrganizationUser.objects.get(
            email=serializer.data["email"], organization__in=[organization_id]
        )
        if not user or not user.check_password(serializer.data["password"]):
            raise NotFound("User not found or invalid credentials.")

        expire = datetime.now() + timedelta(seconds=JWT_EXPIRES_TIME)
        encoded_token = jwt.encode(
            {"email": user.email, "exp": expire}, JWT_SECRET_KEY, algorithm="HS256"
        )
        OrganizationUserAuthHistory.objects.create(
            token=encoded_token, expires_at=expire, user=user
        )

        return Response({"message": "Success", "access_token": encoded_token})


class OrganizationDashboardView(OrganizationDetailGenericView):
    authentication_classes = (OrganizationUserAuthentication,)
    permission_classes = (OrganizationUserPermissionCheck,)

    def post(self, request, organization_id=None):
        organization = self.get_object(organization_id)

        deposits = TransactionResponse(
            data=Transaction.objects.filter(
                organization=organization, transaction_type=TransactionType.DEPOSIT
            ),
            many=True,
        )
        withdrawals = TransactionResponse(
            data=Transaction.objects.filter(
                organization=organization, transaction_type=TransactionType.WITHDRAWAL
            ),
            many=True,
        )
        deposits.is_valid()
        withdrawals.is_valid()
        return Response({"deposits": deposits.data, "withdrawals": withdrawals.data})


class OrganizationDepositView(OrganizationDetailGenericView):
    def post(self, request, organization_id=None):
        serializer = DepositWithdrawalRequest(data=request.data)
        serializer.is_valid(True)

        organization = self.get_object(organization_id)
        transaction = Transaction.objects.create(
            organization=organization,
            transaction_type=TransactionType.DEPOSIT,
            transaction_status=TransactionStatus.INITIATED,
            timestamp=datetime.now(),
            amount=serializer.data["amount"],
        )

        return Response({"message": "Success"})


class OrganizationWithdrawalView(OrganizationDetailGenericView):
    def post(self, request, organization_id=None):
        serializer = DepositWithdrawalRequest(data=request.data)
        serializer.is_valid(True)

        organization = self.get_object(organization_id)
        transaction = Transaction.objects.create(
            organization=organization,
            transaction_type=TransactionType.WITHDRAWAL,
            transaction_status=TransactionStatus.INITIATED,
            timestamp=datetime.now(),
            amount=serializer.data["amount"],
        )

        return Response({"message": "Success"})


class OrganizationApprovementHandleView(OrganizationDetailGenericView):
    authentication_classes = (OrganizationUserAuthentication,)
    permission_classes = (OrganizationUserPermissionCheck,)

    def get_approvement_object(self, organization_id, approvement_id):
        organization = self.get_object(organization_id)
        approvement_obj = Transaction.objects.filter(
            pk=approvement_id,
            organization=organization,
            transaction_status=TransactionStatus.INITIATED,
        ).first()
        if not approvement_obj:
            raise NotFound("Object not found.")
        return approvement_obj

    def get(self, request, organization_id=None, approvement_id=None):
        return Response(
            TransactionResponse(
                self.get_approvement_object(organization_id, approvement_id)
            ).data
        )

    def post(self, request, organization_id=None, approvement_id=None):
        request_serializer = ApprovementRequest(data=request.data)
        request_serializer.is_valid(True)

        transaction = self.get_approvement_object(organization_id, approvement_id)

        if request_serializer.data["status"] == ApprovementRequest.StatusEnum.APPROVED:
            transaction.transaction_status = TransactionStatus.PENDING
        else:
            transaction.transaction_status = TransactionStatus.REJECTED

        TransactionHandle.objects.create(
            managed_user=request.user, transaction=transaction
        )
        transaction.save()

        if transaction.transaction_status == TransactionStatus.PENDING:
            handle_approved_transaction.delay(transaction.pk)
        return Response({"message": "Success."})


class OrganizationApprovementsView(OrganizationDetailGenericView):
    authentication_classes = (OrganizationUserAuthentication,)
    permission_classes = (OrganizationUserPermissionCheck,)

    def get(self, request, organization_id=None):
        organization = self.get_object(organization_id)
        waiting_transactions = TransactionResponse(
            data=Transaction.objects.filter(
                organization=organization,
                transaction_status=TransactionStatus.INITIATED,
            ),
            many=True,
        )
        waiting_transactions.is_valid()
        return Response(waiting_transactions.data)
