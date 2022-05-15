from celery import shared_task
from django.db import DatabaseError, transaction

from core.models.enums.transaction import TransactionStatus, TransactionType
from core.models.transaction import Organization as OrganizationModel
from core.models.transaction import Transaction as TransactionModel


@shared_task
def handle_approved_transaction(transaction_id):

    with transaction.atomic():
        transaction_object = TransactionModel.objects.select_for_update().get(pk=transaction_id, transaction_status=TransactionStatus.PENDING)
        organization_object = OrganizationModel.objects.select_for_update().get(
            pk=transaction_object.organization.pk
        )
        try:
            with transaction.atomic():
                if transaction_object.transaction_type == TransactionType.DEPOSIT:
                    organization_object.balance += transaction_object.amount
                elif transaction_object.transaction_type == TransactionType.WITHDRAWAL:
                    organization_object.balance -= transaction_object.amount

                organization_object.save()
                transaction_object.transaction_status = TransactionStatus.COMPLETED
        except DatabaseError:
            transaction_object.transaction_status = TransactionStatus.ERROR

        transaction_object.save()
