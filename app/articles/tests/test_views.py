import json
from typing import Any, Dict
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status

from app.articles.models import Article

from .mocks import sample_image

User = get_user_model()
fake = Faker()


class TestArticleViews(TestCase):
    """
    Tests for articles app views
    """

    user: Any
    article: Any
    password: str
    data: Dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        """
        setup data to use in the tests
        """
        super().setUpClass()
        cls.password = fake.password()
        cls.user = User.objects.create_user(
            username=fake.name(), email=fake.email(), password=cls.password
        )
        cls.article = Article.objects.create(
            title=fake.name(),
            description=fake.text(),
            body=fake.text(),
            image=sample_image(),
            author=cls.user,
        )

        cls.data = {
            "title": fake.texts(nb_texts=2),
            "description": fake.paragraph(nb_sentences=3),
            "body": fake.paragraph(nb_sentences=20),
            "image": sample_image(),
            "taglist": f"{fake.word()}, {fake.word()}",
        }

    @property
    def bearer_token(self) -> dict:
        """
        Authentication function: logs in user
        """
        login_url = reverse("login")
        response = self.client.post(
            login_url,
            data={"email": self.user.email, "password": self.password},
            format="json",
        )
        token = json.loads(response.content).get("access")
        return {"HTTP_AUTHORIZATION": f"Bearer {token}"}

    @patch(
        "cloudinary.uploader.upload_resource", return_value=fake.image_url()
    )
    def test_create_article(self, upload_resource: Any) -> None:
        """
        Testing creation of articles
        """
        count = Article.objects.count()
        response = self.client.post(
            reverse("create"),
            data=self.data,
            format="json",
            **self.bearer_token,
        )
        self.assertTrue(upload_resource.called)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), count + 1)

    def test_delete_article(self) -> None:
        """
        Test deletion of article by the author
        """
        count = Article.objects.count()
        response = self.client.delete(
            reverse("article-delete", kwargs={"slug": self.article.slug}),
            **self.bearer_token,
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), count - 1)

    def test_delete_article_without_authentication(self) -> None:
        """
        Test deletion of article by a foreign user
        """
        count = Article.objects.count()
        response = self.client.delete(
            reverse("article-delete", kwargs={"slug": self.article.slug}),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Article.objects.count(), count)
        self.assertEqual(
            json.loads(response.content).get("detail"),
            "Authentication credentials were not provided.",
        )
