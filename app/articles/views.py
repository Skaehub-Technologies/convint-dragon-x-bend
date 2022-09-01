from typing import Any

from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from app.articles.filters import ArticleFilter
from app.articles.models import (
    Article,
    ArticleBookmark,
    ArticleComment,
    ArticleHighlight,
    ArticleRatings,
)
from app.articles.permissions import IsOwnerOrReadOnly
from app.articles.serializers import (
    ArticleBookmarkSerializer,
    ArticleCommentSerializer,
    ArticleSerializer,
    ArticleStatSerializer,
    FavouriteSerializer,
    RatingSerializer,
    TextHighlightSerializer,
    UnFavouriteSerializer,
)


class ArticleListView(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]
    filter_backends = [SearchFilter]
    filterset_class = ArticleFilter
    search_fields = [
        "title",
        "description",
        "body",
        "tags__name",
        "author__username",
        "post_id",
    ]


class ArticleListAllView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    filter_backends = [SearchFilter]
    filterset_class = ArticleFilter
    search_fields = [
        "title",
        "description",
        "body",
        "tags__name",
        "author__username",
        "post_id",
    ]


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "slug"

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Returns message on deletion of articles
        """
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Article deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ArticleBookmarkView(generics.ListCreateAPIView):
    serializer_class = ArticleBookmarkSerializer
    queryset = ArticleBookmark.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self) -> Any:
        return (
            super()
            .get_queryset()
            .filter(article_id=self.kwargs.get("article_id"))
        )


class ArticleCommentView(generics.ListCreateAPIView):
    serializer_class = ArticleCommentSerializer
    queryset = ArticleComment.objects.all()
    permission_classes = [IsAuthenticated]
    renderer_classes = (JSONRenderer,)


class ArticleCommentDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ArticleCommentSerializer
    queryset = ArticleComment.objects.all()
    renderer_classes = (JSONRenderer,)
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Returns message on deletion of comments
        """
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Comment deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ArticleRatingsListView(generics.ListCreateAPIView):
    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    serializer_class = RatingSerializer
    queryset = ArticleRatings.objects.all()
    renderer_classes = (JSONRenderer,)
    lookup_field = "article_id"

    def get_queryset(self) -> Any:
        return (
            super()
            .get_queryset()
            .filter(article_id=self.kwargs.get("article_id"))
        )


class ArticleFavouriteView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FavouriteSerializer
    queryset = Article.objects.all()
    lookup_field = "slug"
    renderer_classes = (JSONRenderer,)


class ArticleUnFavouriteView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UnFavouriteSerializer
    queryset = Article.objects.all()
    lookup_field = "slug"
    renderer_classes = (JSONRenderer,)


class HighlightArticleListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TextHighlightSerializer
    queryset = ArticleHighlight.objects.all()
    renderer_classes = (JSONRenderer,)


class HiglightDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TextHighlightSerializer
    queryset = ArticleHighlight.objects.all()
    renderer_classes = (JSONRenderer,)
    lookup_field = "id"

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Returns message on deletion of highlights
        """
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Highlight comment deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ArticleStatsView(generics.ListAPIView):
    serializer_class = ArticleStatSerializer
    queryset = Article.objects.all()
    renderer_classes = (JSONRenderer,)
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self) -> Any:
        return super().get_queryset().filter(slug=self.kwargs.get("slug"))
