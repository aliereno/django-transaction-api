from django.db import models

from core.models.enums.transaction import TransactionStatus, TransactionType
from core.models.organization import Organization, OrganizationUser


class Transaction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    transaction_type = models.PositiveSmallIntegerField(choices=TransactionType.choices)
    transaction_status = models.PositiveSmallIntegerField(
        choices=TransactionStatus.choices
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)


class TransactionHandle(models.Model):
    managed_user = models.ForeignKey(OrganizationUser, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
