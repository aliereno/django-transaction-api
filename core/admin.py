from django.contrib import admin

from core.models.organization import (
    Organization,
    OrganizationUser,
    OrganizationUserAuthHistory,
    OrganizationUserPermission,
)
from core.models.transaction import Transaction, TransactionHandle


class OrganizationUserAdmin(admin.ModelAdmin):
    exclude = ("password",)


admin.site.register(Organization)
admin.site.register(OrganizationUser, OrganizationUserAdmin)
admin.site.register(OrganizationUserAuthHistory)
admin.site.register(OrganizationUserPermission)
admin.site.register(Transaction)
admin.site.register(TransactionHandle)
