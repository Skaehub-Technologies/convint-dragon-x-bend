import uuid
from typing import Any

from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from app.abstracts import TimeStampedModel

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
    favourited = models.BooleanField(null=True)
    favouritesCount = models.BigIntegerField(
        blank=True,
        default=0,
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


class ArticleBookmark(TimeStampedModel):
    """
    Bookmark model to store the articles bookmarked by a reader
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
