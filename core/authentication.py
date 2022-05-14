from datetime import datetime

import jwt
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission

from app.settings import JWT_SECRET_KEY
from core.models.organization import (
    OrganizationUserAuthHistory,
    OrganizationUserPermission,
)


def get_view_name(viewname):
    result = viewname.split(" object")[0][1:]
    return result


class OrganizationUserPermissionCheck(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        print(f"**checking permission on viewname: `{get_view_name(view.__str__())}`")
        check_permission = OrganizationUserPermission.objects.filter(
            view_name=get_view_name(view.__str__()), user=request.user, organization=obj
        )
        if not check_permission:
            return False
        return True


class OrganizationUserAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            return None
        try:
            now = datetime.now()
            ua = (
                OrganizationUserAuthHistory.objects.order_by("-id")
                .filter(token=token, expires_at__gt=now)
                .get()
            )
        except OrganizationUserAuthHistory.DoesNotExist:
            raise AuthenticationFailed("Unauthorized")
        return (ua.user, None)
