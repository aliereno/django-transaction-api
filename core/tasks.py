from celery import shared_task
from django.db import DatabaseError, transaction

from core.models.enums.transaction import TransactionStatus, TransactionType
from core.models.transaction import Transaction as TransactionModel


@shared_task
def handle_approved_transaction(transaction_id):

    transaction_object = TransactionModel.objects.get(pk=transaction_id)
    try:
        with transaction.atomic():
            organization = transaction_object.organization
            if transaction_object.transaction_type == TransactionType.DEPOSIT:
                organization.balance += transaction_object.amount
            elif transaction_object.transaction_type == TransactionType.WITHDRAWAL:
                organization.balance -= transaction_object.amount

            organization.save()
            transaction_object.transaction_status = TransactionStatus.COMPLETED
    except DatabaseError:
        transaction_object.transaction_status = TransactionStatus.ERROR

    transaction_object.save()
