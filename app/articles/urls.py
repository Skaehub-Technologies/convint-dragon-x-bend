from django.urls import path

from app.articles.views import (
    ArticleDetailView,
    ArticleListCreateView,
    ArticleRatingsListCreateView,
)

urlpatterns = [
    path("article/", ArticleListCreateView.as_view(), name="article-list"),
    path(
        "article/<slug:slug>/",
        ArticleDetailView.as_view(),
        name="article-detail",
    ),
    path("rate/", ArticleRatingsListCreateView.as_view(), name="rate"),
]
