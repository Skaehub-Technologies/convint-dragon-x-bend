from django.urls import path

from app.articles.views import (
    ArticleBookmarkView,
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
    path("bookmarks/", ArticleBookmarkView.as_view(), name="bookmark"),
    path("rate/", ArticleRatingsListCreateView.as_view(), name="rate"),
]
