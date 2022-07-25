from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from app.articles.models import Article
from app.user.serializers import UserSerializer

User = get_user_model()


class ArticlesSerializers(TaggitSerializer, serializers.ModelSerializer):  # type: ignore[no-any-unimported]
    author = UserSerializer(read_only=True)
    title = serializers.CharField(max_length=100, min_length=20, required=True)
    description = serializers.CharField(
        max_length=255, min_length=20, required=True
    )
    image = serializers.ImageField(use_url=True, required=False)
    body = serializers.CharField(max_length=255, min_length=20, required=True)
    taglist = TagListSerializerField()

    class Meta:
        model = Article
        fields = (
            "article_id",
            "author",
            "title",
            "description",
            "image",
            "body",
            "taglist",
            "favourited",
            "favouritesCount",
            "slug",
        )
        read_only_fields = [
            "created_at",
            "updated_at",
            "author",
            "favouritesCount",
            "favourited",
        ]

    def create(self, validated_data: Any) -> Any:
        """set current user as author"""
        validated_data["author"] = self.context.get("request").user  # type: ignore[union-attr]
        return super().create(validated_data)
