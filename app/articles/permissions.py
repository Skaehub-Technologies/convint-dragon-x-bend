from typing import Any

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class AuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> Any:
        return request.user.is_authenticated

    def has_object_permission(
        self, request: Request, view: APIView, obj: Any
    ) -> Any:
        return obj.author == request.user
