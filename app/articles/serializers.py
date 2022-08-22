from collections import Counter
from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import serializers

from app.articles.models import (
    Article,
    ArticleBookmark,
    ArticleComment,
    ArticleHighlight,
    ArticleRatings,
    Tag,
)
from app.user.serializers import UserSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=50,
    )

    class Meta:
        model = Tag
        fields = ("name",)


class ArticleSerializer(serializers.ModelSerializer):
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
    avg_rating = serializers.SerializerMethodField(
        method_name="average_rating"
    )
    favourite_count = serializers.SerializerMethodField()
    unfavourite_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            "post_id",
            "reading_time",
            "author",
            "title",
            "description",
            "image",
            "body",
            "tags",
            "taglist",
            "slug",
            "avg_rating",
            "favourite_count",
            "unfavourite_count",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "created_at",
            "updated_at",
            "author",
            "tags",
            "reading_time",
        )

    def create(self, validated_data: Any) -> Any:
        """set current user as author"""
        validated_data["author"] = self.context.get("request").user  # type: ignore[union-attr]
        taglist = validated_data.pop("taglist")
        article = super().create(validated_data)
        tags = []
        for name in taglist.split(","):
            tag, _ = Tag.objects.get_or_create(name=name.strip())
            tags.append(tag)
        article.tags.set(tags)

        return article

    def average_rating(self, instance):  # type: ignore[no-untyped-def]
        avg_rating = (
            ArticleRatings.objects.filter(article=instance).aggregate(
                average_rating=Avg("rating")
            )["average_rating"]
            or 0
        )
        avg_rating = round(avg_rating)
        total_user_rates = ArticleRatings.objects.filter(
            article=instance
        ).count()
        each_rating = Counter(
            ArticleRatings.objects.filter(article=instance).values_list(
                "rating", flat=True
            )
        )

        return {
            "avg_rating": avg_rating,
            "total_user_rates": total_user_rates,
            "each_rating": each_rating,
        }

    def get_favourite_count(self, instance: Any) -> Any:
        return instance.favourite.count()

    def get_unfavourite_count(self, instance: Any) -> Any:
        return instance.unfavourite.count()


class ArticleBookmarkSerializer(serializers.ModelSerializer):
    """
    Bookmarks serializer
    """

    user = UserSerializer(read_only=True)
    article = serializers.SlugRelatedField(
        queryset=Article.objects.all(), slug_field="post_id"
    )

    class Meta:
        model = ArticleBookmark
        fields = ("article", "user")

    def create(self, validated_data: Any) -> Any:
        request = self.context["request"]

        validated_data["user"] = request.user
        instance, _ = ArticleBookmark.objects.get_or_create(**validated_data)

        return instance


class ArticleCommentSerializer(serializers.ModelSerializer):
    """
    Comment and highlighting serializer
    """

    commenter = UserSerializer(read_only=True)

    class Meta:
        model = ArticleComment
        fields = (
            "id",
            "commenter",
            "comment",
            "article",
            "created_at",
        )
        read_only_fields = (
            "created_at",
            "commenter",
            "id",
        )

    def create(self, validated_data: Any) -> Any:
        request = self.context["request"]
        validated_data["commenter"] = request.user
        instance = ArticleComment.objects.create(**validated_data)
        return instance


class RatingSerializer(serializers.ModelSerializer):
    """
    create and update existing ratings for our articles
    """

    rating = serializers.IntegerField(max_value=5, min_value=0)
    rated_by = UserSerializer(read_only=True)
    article = serializers.SlugRelatedField(
        queryset=Article.objects.all(), slug_field="post_id"
    )

    class Meta:
        model = ArticleRatings
        fields = ["rating", "rated_by", "article"]
        read_only_fields = ["rated_by"]

    def create(self, validated_data: Any) -> Any:
        request = self.context["request"]

        validated_data["rated_by"] = request.user
        instance = ArticleRatings.objects.create(**validated_data)

        return instance


class FavouriteSerializer(serializers.Serializer):
    def update(self, instance: Any, validated_data: Any) -> Any:
        """
        update the favourites of an article
        """
        request = self.context.get("request")

        if request.user in instance.favourite.all():  # type: ignore[union-attr]
            instance.favourite.remove(request.user)  # type: ignore[union-attr]
            return instance
        if request.user in instance.unfavourite.all():  # type: ignore[union-attr]
            instance.unfavourite.remove(request.user)  # type: ignore[union-attr]
        instance.favourite.add(request.user)  # type: ignore[union-attr]
        return instance


class UnFavouriteSerializer(serializers.Serializer):
    def update(self, instance: Any, validated_data: Any) -> Any:
        """update the unfavourites of an article"""
        request = self.context.get("request")

        if request.user in instance.unfavourite.all():  # type: ignore[union-attr]
            instance.unfavourite.remove(request.user)  # type: ignore[union-attr]
            return instance
        if request.user in instance.favourite.all():  # type: ignore[union-attr]
            instance.favourite.remove(request.user)  # type: ignore[union-attr]
        instance.unfavourite.add(request.user)  # type: ignore[union-attr]
        return instance


class TextHighlightSerializer(serializers.ModelSerializer):
    """
    Highlights model serializer
    """

    highlighter = UserSerializer(read_only=True)
    article = serializers.SlugRelatedField(
        queryset=Article.objects.all(), slug_field="post_id"
    )
    highlight_start = serializers.IntegerField(
        min_value=0,
    )
    highlight_end = serializers.IntegerField(
        min_value=0,
    )
    highlight_text = serializers.CharField(read_only=True)

    class Meta:
        model = ArticleHighlight
        fields = (
            "id",
            "comment",
            "article",
            "highlighter",
            "highlight_start",
            "highlight_end",
            "highlight_text",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "highlighter",
            "id",
            "created_at",
            "updated_at",
        )

    def validate(self, data: Any) -> Any:

        article = data.get("article")
        if data.get("highlight_start") > len(article.body):
            raise serializers.ValidationError(
                {
                    "highlight_start": "This field should be less than the length of the article"
                },
                code="invalid_length",
            )
        if data.get("highlight_end") > len(article.body):
            raise serializers.ValidationError(
                {
                    "highlight_end": "This field should be less than the length of the article"
                },
                code="invalid_length",
            )

        return data

    def create(self, validated_data: Any) -> Any:
        article = validated_data.get("article")
        validated_data["highlighter"] = self.context.get("request").user  # type: ignore[union-attr]
        start = validated_data.get("highlight_start")
        end = validated_data.get("highlight_end")
        if start > end:
            start, end = end, start
            highlight_text = str(article.body[start:end])
            validated_data["highlight_text"] = highlight_text

        return super().create(validated_data)


class ArticleStatSerializer(serializers.ModelSerializer):
    """
    Serializer class for reading stats
    """

    comment_count = serializers.SerializerMethodField()
    favourite_count = serializers.SerializerMethodField()
    unfavourite_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()

    def get_comment_count(self, instance: Any) -> Any:
        return ArticleComment.objects.filter(article=instance).count()

    def get_bookmark_count(self, instance: Any) -> Any:
        return ArticleBookmark.objects.filter(article=instance).count()

    def get_favourite_count(self, instance: Any) -> Any:
        return instance.favourite.count()

    def get_unfavourite_count(self, instance: Any) -> Any:
        return instance.unfavourite.count()

    def get_average_rating(self, instance: Any) -> Any:
        return (
            ArticleRatings.objects.filter(article=instance).aggregate(
                average_rating=Avg("rating")
            )["average_rating"]
            or 0
        )

    class Meta:
        model = Article
        fields = [
            "slug",
            "title",
            "comment_count",
            "bookmark_count",
            "favourite_count",
            "unfavourite_count",
            "average_rating",
        ]
