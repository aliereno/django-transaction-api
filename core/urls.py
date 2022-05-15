from django.urls import path

from core.views import organization

urlpatterns = [
    path(
        "organization/<str:organization_id>/auth",
        organization.OrganizationAuthenticateView.as_view(),
        name="organization_authenticate",
    ),
    path(
        "organization/<str:organization_id>/dashboard",
        organization.OrganizationDashboardView.as_view(),
        name="organization_dashboard",
    ),
    path(
        "organization/<str:organization_id>/deposit",
        organization.OrganizationDepositView.as_view(),
        name="organization_customer_deposit",
    ),
    path(
        "organization/<str:organization_id>/withdrawal",
        organization.OrganizationWithdrawalView.as_view(),
        name="organization_customer_withdrawal",
    ),
    path(
        "organization/<str:organization_id>/approvements/<str:approvement_id>",
        organization.OrganizationApprovementHandleView.as_view(),
        name="organization_approvement_handle",
    ),
    path(
        "organization/<str:organization_id>/approvements",
        organization.OrganizationApprovementsView.as_view(),
        name="organization_approvement_list",
    ),
]
