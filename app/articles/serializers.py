from collections import Counter
from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import serializers

from app.articles.models import Article, ArticleBookmark, ArticleRatings, Tag
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
