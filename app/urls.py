from django.urls import include, path

urlpatterns = [
    path("user/"), include("app.user.urls"),
]
