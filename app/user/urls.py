from django.urls import path

from . import views

urlpatterns = [
    path('profile_details/', views.ProfileDetails.as_view(), name='add_profile_details'),
    path('show_profile/<str:pk>/', views.ViewsProfile.as_view(), name="view_profile"),
    path('follow_profile/<str:user_pk>/', views.FollowProfile.as_view(), name="follow_profile"),
    path('unfollow_profile/<str:user_pk>/', views.UnFollowProfile.as_view(), name="unfollow_profile"),
    path('view_followers/<str:pk>/', views.ViewFollowers.as_view(), name="view_followers"),
    path('view_followings/<str:pk>/', views.ViewFollowings.as_view(), name="view_followings"),
]
