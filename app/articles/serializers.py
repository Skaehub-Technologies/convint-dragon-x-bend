from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.articles.models import Article, Tag
from app.user.serializers import UserSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=50,
    )

    class Meta:
        model = Tag
        fields = ("name",)


class ArticlesSerializers(serializers.ModelSerializer):
    post_id = serializers.CharField(
        read_only=True,
    )
    author = UserSerializer(read_only=True)
    title = serializers.CharField(
        max_length=400,
        min_length=20,
    )
    description = serializers.CharField(
        max_length=255,
        min_length=20,
    )
    image = serializers.ImageField(use_url=True, required=False)
    body = serializers.CharField(
        min_length=20,
    )
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )  # type: ignore[var-annotated]
    taglist = serializers.CharField(
        write_only=True,
    )

    class Meta:
        model = Article
        fields = (
            "post_id",
            "author",
            "title",
            "description",
            "image",
            "body",
            "tags",
            "taglist",
            "favourited",
            "favouritesCount",
            "slug",
        )
        read_only_fields = (
            "created_at",
            "updated_at",
            "author",
            "tags",
            "favouritesCount",
            "favourited",
        )

    def create(self, validated_data: Any) -> Any:
        """set current user as author"""
        validated_data["author"] = self.context.get("request").user  # type: ignore[union-attr]
        tags = validated_data.pop("taglist")
        article = super().create(validated_data)
        for name in tags.split(","):
            tag, _ = Tag.objects.get_or_create(name=name.strip())
            article.tags.add(tag)

        return article
