from typing import Any

from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

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


class ArticleListCreateView(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    filterset_fields = ["title", "description", "body", "tags", "author"]
    filter_backends = [SearchFilter]
    search_fields = ["title", "description", "body", "tags", "author"]


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
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class ArticleCommentView(generics.ListCreateAPIView):
    serializer_class = ArticleCommentSerializer
    queryset = ArticleComment.objects.all()
    permission_classes = [IsAuthenticated]


class ArticleCommentDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ArticleCommentSerializer
    queryset = ArticleComment.objects.all()
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


class ArticleRatingsListCreateView(generics.ListCreateAPIView):
    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    serializer_class = RatingSerializer
    queryset = ArticleRatings.objects.all()


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

class ArticleStatsView(generics.ListCreateAPIView):
    serializer_class = ArticleStatSerializer
    queryset = Article.objects.all()
    renderer_classes = (JSONRenderer,)
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self) -> Any:
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)
class HighlightArticleListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TextHighlightSerializer
    queryset = ArticleHighlight.objects.all()


class HiglightDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TextHighlightSerializer
    queryset = ArticleHighlight.objects.all()
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
