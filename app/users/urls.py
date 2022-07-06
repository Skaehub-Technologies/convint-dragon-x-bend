from django.urls import path

from app.users.views import ( 
    UserFollowerView, 
    UserFollowingView  
) 

app_name = 'users'

urlpatterns = [
    path('users/UserFollower', UserFollowerView.as_view()),
    path('users/UserFollowing', UserFollowingView.as_view()),

]
