from django.urls import path

from app.articles.views import (
    ArticleCreateView,
    ArticleDetailView,
    ArticleListView,
)

urlpatterns = [
    path("all-articles/", ArticleListView.as_view(), name="articles"),
    path(
        "update/<slug:slug>/detail/",
        ArticleDetailView.as_view(),
        name="article-update",
    ),
    path(
        "delete/<slug:slug>/detail/",
        ArticleDetailView.as_view(),
        name="article-delete",
    ),
    path("create/", ArticleCreateView.as_view(), name="create"),
]
