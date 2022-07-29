from typing import Any

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsUser(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: APIView, obj: Any
    ) -> bool:
        return bool(obj.user == request.user)
