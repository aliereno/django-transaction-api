from django.db import models


class TransactionType(models.IntegerChoices):
    DEPOSIT = 1, "Deposit"
    WITHDRAWAL = 2, "Withdrawal"


class TransactionStatus(models.IntegerChoices):
    INITIATED = 0, "Initiated"
    PENDING = 1, "Pending"
    COMPLETED = 2, "Completed"
    FAILED = 3, "Failed"
    ERROR = 4, "Error"
    REJECTED = 5, "Rejected"
