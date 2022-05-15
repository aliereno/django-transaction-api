from django.contrib import admin
from django.http import HttpResponse

from core.models.organization import (
    Organization,
    OrganizationUser,
    OrganizationUserAuthHistory,
    OrganizationUserPermission,
)
from core.models.transaction import Transaction, TransactionHandle


class TransactionAdmin(admin.ModelAdmin):
    def download_csv(modeladmin, request, queryset):
        import csv

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=transactions.csv"

        writer = csv.writer(response)
        writer.writerow(
            [
                "timestamp",
                "amount",
                "transaction_type",
                "transaction_status",
                "organization_id",
                "organization_title",
            ]
        )
        for s in queryset:
            writer.writerow(
                [
                    s.timestamp,
                    s.amount,
                    s.transaction_type,
                    s.transaction_status,
                    s.organization.pk,
                    s.organization.title,
                ]
            )

        return response

    list_display = (
        "timestamp",
        "amount",
        "transaction_type",
        "transaction_status",
        "organization",
    )
    list_filter = ("organization",)
    actions = [download_csv]


class OrganizationUserAdmin(admin.ModelAdmin):
    exclude = ("password",)


admin.site.register(Organization)
admin.site.register(OrganizationUser, OrganizationUserAdmin)
admin.site.register(OrganizationUserAuthHistory)
admin.site.register(OrganizationUserPermission)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(TransactionHandle)
