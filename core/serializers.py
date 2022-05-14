from django.db import models
from rest_framework import serializers

from core.models.transaction import Transaction


class AuthenticateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class DepositWithdrawalRequest(serializers.Serializer):
    amount = serializers.DecimalField(required=True, max_digits=12, decimal_places=2)


class ApprovementRequest(serializers.Serializer):
    class StatusEnum(models.IntegerChoices):
        REJECTED = -1, "Rejected"
        APPROVED = 1, "Approved"

    status = serializers.ChoiceField(required=True, choices=StatusEnum)


class TransactionResponse(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "timestamp", "amount", "transaction_type", "transaction_status"]
