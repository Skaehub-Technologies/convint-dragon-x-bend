from django.urls import path

from app.articles.views import ArticleDetailView, ArticleListCreateView

urlpatterns = [
    path("all-articles/", ArticleListCreateView.as_view(), name="articles"),
    path(
        "article/<slug:slug>/detail/",
        ArticleDetailView.as_view(),
        name="article-update",
    ),
    path(
        "delete/<slug:slug>/detail/",
        ArticleDetailView.as_view(),
        name="article-delete",
    ),
    path("create/", ArticleListCreateView.as_view(), name="create"),
]
