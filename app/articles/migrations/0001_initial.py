# Generated by Django 4.0.6 on 2022-07-27 08:43

import uuid

import cloudinary.models
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Article",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "post_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                ("title", models.CharField(max_length=400)),
                (
                    "image",
                    cloudinary.models.CloudinaryField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="post_images",
                    ),
                ),
                (
                    "description",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("body", models.TextField()),
                ("favourited", models.BooleanField(null=True)),
                (
                    "favouritesCount",
                    models.IntegerField(
                        blank=True,
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0)
                        ],
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="author",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        blank=True, related_name="tags", to="articles.tag"
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
