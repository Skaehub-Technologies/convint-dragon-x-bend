from django.urls import path

from app.user.views import UserFollow


urlpatterns = [
   path(
        "follow/<int:pk>/", UserFollow.as_view(), name="user-follow"
    ),
]
