from typing import Any

from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from app.articles.models import Article, ArticleRatings
from app.articles.permissions import AuthorOrReadOnly
from app.articles.serializers import ArticleSerializer, RatingSerializer


class ArticleListCreateView(generics.ListCreateAPIView):
    permission_classes = [
        IsAuthenticated,
        AuthorOrReadOnly,
    ]

    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    filterset_fields = [
        "title",
        "description",
        "body",
        "tags",
        "author__username",
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "title",
        "description",
        "body",
        "tags",
        "author__username",
    ]


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticated,
        AuthorOrReadOnly,
    ]
    serializer_class = ArticleSerializer
    lookup_field = "slug"
    queryset = Article.objects.all()

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Returns message on deletion of articles
        """
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Article deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ArticleRatingsListCreateView(generics.ListCreateAPIView):
    permission_classes = [
        IsAuthenticated,
        AuthorOrReadOnly,
    ]

    serializer_class = RatingSerializer
    queryset = ArticleRatings.objects.all()
