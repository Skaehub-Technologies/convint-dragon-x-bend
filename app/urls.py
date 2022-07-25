from django.urls import include, path

urlpatterns = [
    path("user/", include("app.user.urls")),
    path("articles/", include("app.articles.urls")),
]
