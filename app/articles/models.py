import math
import uuid
from typing import Any

from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from app.abstracts import TimeStampedModel, UniversalIdModel

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Article(TimeStampedModel):
    post_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        max_length=255,
        primary_key=True,
    )
    slug = models.SlugField(max_length=400, unique=True, blank=True, null=True)
    title = models.CharField(max_length=400, blank=False, null=False)
    image = CloudinaryField("post_images", blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    body = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, related_name="tags")
    favouritesCount = models.BigIntegerField(
        blank=True,
        default=0,
    )
    reading_time = models.PositiveIntegerField(blank=True, null=True)
    favourite = models.ManyToManyField(
        User, related_name="favourite", blank=True
    )
    unfavourite = models.ManyToManyField(
        User, related_name="unfavourite", blank=True
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="author", null=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


@receiver(pre_save, sender=Article)
def slug_pre_save(sender: Any, instance: Any, **kwargs: Any) -> None:
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(f"{instance.title}-{instance.post_id}")


@receiver(pre_save, sender=Article)
def reading_time_pre_save(sender: Any, instance: Any, **kwargs: Any) -> None:
    instance.reading_time = math.ceil(instance.body.count(" ") // 200)


class ArticleBookmark(TimeStampedModel):
    """
    Bookmark model to store the articles bookmarked by a reader
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class ArticleComment(TimeStampedModel, UniversalIdModel):
    """
    Comment model to store comments made on articles
    """

    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.TextField()

    class Meta:
        ordering = ["created_at"]


class ArticleHighlight(TimeStampedModel, UniversalIdModel):
    """
    Highlights for any text
    """

    highlight_start = models.PositiveIntegerField()
    highlight_end = models.PositiveIntegerField()
    highlight_text = models.TextField()
    comment = models.TextField()
    highlighter = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]


class ArticleRatings(models.Model):
    """
    Ratings given by different users
    """

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE)
