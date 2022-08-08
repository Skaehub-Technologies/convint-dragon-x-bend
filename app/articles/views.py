from typing import Any

from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from app.articles.models import Article, ArticleBookmark, ArticleRatings
from app.articles.permissions import IsOwnerOrReadOnly
from app.articles.serializers import (
    ArticleBookmarkSerializer,
    ArticleSerializer,
    FavouriteSerializer,
    RatingSerializer,
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
