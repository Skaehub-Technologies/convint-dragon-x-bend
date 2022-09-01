from django.urls import path

from app.articles.views import (
    ArticleBookmarkView,
    ArticleCommentDetailView,
    ArticleCommentView,
    ArticleDetailView,
    ArticleFavouriteView,
    ArticleListAllView,
    ArticleListView,
    ArticleRatingsListView,
    ArticleStatsView,
    ArticleUnFavouriteView,
    HighlightArticleListView,
    HiglightDetailView,
)

urlpatterns = [
    path("article/", ArticleListView.as_view(), name="article-list"),
    path("articles/", ArticleListAllView.as_view(), name="all-articles"),
    path(
        "article/<slug:slug>/",
        ArticleDetailView.as_view(),
        name="article-detail",
    ),
    path("bookmarks/", ArticleBookmarkView.as_view(), name="bookmark"),
    path(
        "articles/<str:article_id>/bookmarks/",
        ArticleBookmarkView.as_view(),
        name="article-bookmark",
    ),
    path("comments/", ArticleCommentView.as_view(), name="comment"),
    path(
        "comments/<str:id>/",
        ArticleCommentDetailView.as_view(),
        name="comment-delete",
    ),
    path("rate/", ArticleRatingsListView.as_view(), name="rate"),
    path(
        "articles/<str:article_id>/rate/",
        ArticleRatingsListView.as_view(),
        name="article-rates",
    ),
    path(
        "articles/<slug:slug>/favourite/",
        ArticleFavouriteView.as_view(),
        name="favourite",
    ),
    path(
        "articles/<slug:slug>/unfavourite/",
        ArticleUnFavouriteView.as_view(),
        name="unfavourite",
    ),
    path(
        "articles/<slug:slug>/stats/",
        ArticleStatsView.as_view(),
        name="statistics",
    ),
    path(
        "highlight/",
        HighlightArticleListView.as_view(),
        name="highlight",
    ),
    path(
        "highlight/<str:id>/",
        HiglightDetailView.as_view(),
        name="highlight-detail",
    ),
]
