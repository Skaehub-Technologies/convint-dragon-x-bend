from typing import Any

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from app.articles.models import Article
from rest_framework import filters
from app.articles.permissions import AuthorOrReadOnly
from app.articles.serializers import ArticlesSerializers


class ArticleListCreateView(generics.ListCreateAPIView):
    permission_classes = [
        IsAuthenticated,
        AuthorOrReadOnly,
    ]
    serializer_class = ArticlesSerializers
    queryset = Article.objects.all()
    filterset_fields = ['title', 'description', 'body', 'tags', 'author']
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'body', 'tags', 'author']


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticated,
        AuthorOrReadOnly,
    ]
    serializer_class = ArticlesSerializers
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
