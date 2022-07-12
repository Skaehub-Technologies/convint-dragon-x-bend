from django.urls import path

from app.user.views import UserFollowView

urlpatterns = [
    path("follow/<int:pk>/", UserFollowView.as_view(), name="follow"),
    path("unfollow/<int:pk>/", UserFollowView.as_view(), name="unfollow"),
]
