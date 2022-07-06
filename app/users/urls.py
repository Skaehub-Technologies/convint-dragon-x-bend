from django.urls import path

from app.users.views import ( 
    UserFollowerView, 
    UserFollowingView  
) 

urlpatterns = [
    path(
       "users/follow/",UserFollowerView.as_view(), name="user-follow"
    ),
    path(
        "users/following/", UserFollowingView.as_view(), name="user-following"
    ),
]