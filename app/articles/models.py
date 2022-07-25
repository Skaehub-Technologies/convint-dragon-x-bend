import uuid
from typing import Any

from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from taggit.managers import TaggableManager

from app.abstracts import TimeStampedModel

User = get_user_model()


class Article(TimeStampedModel):
    article_id = models.UUIDField(
        default=uuid.uuid4().hex, editable=False, unique=True, max_length=255
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    title = models.CharField(max_length=100, blank=False, null=False)
    image = CloudinaryField("post_images", blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    body = models.CharField(max_length=255, blank=False, null=False)
    taglist = TaggableManager()
    favourited = models.BooleanField(null=True)
    favouritesCount = models.IntegerField(
        blank=True, default=0, validators=[MinValueValidator(0)]
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
        instance.slug = slugify(f"{instance.title}-{instance.article_id}")
