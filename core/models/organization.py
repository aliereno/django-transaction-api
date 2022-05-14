from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class OrganizationUser(AbstractBaseUser):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField()

    USERNAME_FIELD = "email"


class Organization(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    balance = models.DecimalField(decimal_places=2, max_digits=12)

    users = models.ManyToManyField(OrganizationUser, related_name="organization")


class OrganizationUserAuthHistory(models.Model):
    token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
    user = models.ForeignKey(OrganizationUser, on_delete=models.CASCADE)


class OrganizationUserPermission(models.Model):
    view_name = models.CharField(max_length=255)
    user = models.ForeignKey(OrganizationUser, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
