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
            reverse("article-list"),
            data=self.data,
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
            reverse("article-detail", kwargs={"slug": self.article.slug}),
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
            reverse("article-detail", kwargs={"slug": self.article.slug}),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Article.objects.count(), count)
        self.assertEqual(
            json.loads(response.content).get("detail"),
            "Authentication credentials were not provided.",
        )


class TestBookmarkView(TestCase):
    password: str
    user: Any

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.password = fake.password()
        cls.user = User.objects.create_user(
            username=fake.name(), email=fake.email(), password=cls.password
        )

    @property
    def bearer_token(self) -> dict:
        login_url = reverse("login")
        response = self.client.post(
            login_url,
            data={"email": self.user.email, "password": self.password},
        )
        token = json.loads(response.content).get("access")
        return {"HTTP_AUTHORIZATION": f"Bearer {token}"}

    def test_bookmark_article(self) -> None:
        """
        Test if a user can bookmark an article
        """
        data = Article.objects.create(
            post_id="9831040d-5eeb-4cd5-9054-d0f1770431ca",
            title=fake.texts(nb_texts=2),
            description=fake.paragraph(nb_sentences=3),
            body=fake.paragraph(),
        )

        response = self.client.post(
            reverse("bookmark"),
            data={"article": data.post_id},
            **self.bearer_token,
        )
        res_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_data["article"], data.post_id)

    def test_get_bookmark(self) -> None:
        """
        Test if user can get their bookmarks
        """
        data = Article.objects.create(
            post_id="9831040d-5eeb-4cd5-9054-d0f1770431ca",
            title=fake.texts(nb_texts=2),
            description=fake.paragraph(nb_sentences=3),
            body=fake.paragraph(),
        )

        response = self.client.post(
            reverse("bookmark"),
            data={"article": data.post_id},
            **self.bearer_token,
        )
        res_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_data["article"], data.post_id)

        response = self.client.get(
            reverse("bookmark"),
            **self.bearer_token,
        )
        res = response.json().get("results")[0].get("article")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(res, data.post_id)


class TestArticleRatingView(TestCase):
    password: str
    user: Any
    article: Any

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.password = fake.password()
        cls.user = User.objects.create_user(
            username=fake.name(), email=fake.email(), password=cls.password
        )
        cls.article = Article.objects.create(
            title=fake.texts(nb_texts=1),
            description=fake.paragraph(nb_sentences=1),
            body=fake.paragraph(),
        )

    @property
    def bearer_token(self) -> dict:
        login_url = reverse("login")
        response = self.client.post(
            login_url,
            data={"email": self.user.email, "password": self.password},
        )
        token = json.loads(response.content).get("access")
        return {"HTTP_AUTHORIZATION": f"Bearer {token}"}

    def test_rate_article(self) -> None:
        """
        Test if a user can Rate an article
        """
        response = self.client.post(
            reverse("rate"),
            data={"article": self.article.post_id, "rating": 1},
            **self.bearer_token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("article"), self.article.post_id)  # type: ignore[attr-defined]

    def test_rate_article_unauthorized(self) -> None:
        """
        Test if a user can Rate an article
        """
        response = self.client.post(
            reverse("rate"),
            data={"article": self.article.post_id, "rating": 1},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            json.loads(response.content).get("detail"),
            "Authentication credentials were not provided.",
        )

    def test_get_rating(self) -> None:
        """
        Test if user can get their ratings
        """
        response = self.client.post(
            reverse("rate"),
            data={"article": self.article.post_id, "rating": 1},
            **self.bearer_token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("article"), self.article.post_id)  # type: ignore[attr-defined]

        response = self.client.get(
            reverse("rate"),
            **self.bearer_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_rate_unauthorized(self) -> None:
        """
        Test if a user can get article rating unauthorized
        """
        response = self.client.get(
            reverse("rate"),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            json.loads(response.content).get("detail"),
            "Authentication credentials were not provided.",
        )


class TestArticleFavouriteUnfavouriteView(TestCase):
    password: str
    user: Any
    article: Any

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.password = fake.password()
        cls.user = User.objects.create_user(
            username=fake.name(), email=fake.email(), password=cls.password
        )
        cls.article = Article.objects.create(
            title=fake.texts(nb_texts=1),
            description=fake.paragraph(nb_sentences=1),
            body=fake.paragraph(),
        )

    @property
    def bearer_token(self) -> dict:
        login_url = reverse("login")
        response = self.client.post(
            login_url,
            data={"email": self.user.email, "password": self.password},
        )
        token = json.loads(response.content).get("access")
        return {"HTTP_AUTHORIZATION": f"Bearer {token}"}

    def test_favourite_article(self) -> None:
        """test favourite an article"""
        favourite = self.article.favourite.count()
        response = self.client.patch(
            reverse("favourite", kwargs={"slug": self.article.slug}),
            **self.bearer_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.favourite.count(), favourite + 1)

    def test_favourite_article_unauthorized(self) -> None:
        """
        test favourite an article without authentication
        """
        response = self.client.patch(
            reverse("favourite", kwargs={"slug": self.article.slug}),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            json.loads(response.content).get("detail"),
            "Authentication credentials were not provided.",
        )

    def test_unfavourite_article(self) -> None:
        """test unfavourite an article"""
        unfavourite = self.article.unfavourite.count()
        response = self.client.patch(
            reverse("unfavourite", kwargs={"slug": self.article.slug}),
            **self.bearer_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.unfavourite.count(), unfavourite + 1)

    def test_unfavourite_article_unauthorized(self) -> None:
        """
        test unfavourite an article without authentication
        """
        response = self.client.patch(
            reverse("unfavourite", kwargs={"slug": self.article.slug}),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            json.loads(response.content).get("detail"),
            "Authentication credentials were not provided.",
        )

    def test_favourite_twice_article(self) -> None:
        """test favourite an article"""
        favourite = self.article.favourite.count()
        response = self.client.patch(
            reverse("favourite", kwargs={"slug": self.article.slug}),
            **self.bearer_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.favourite.count(), favourite + 1)
        response = self.client.patch(
            reverse("favourite", kwargs={"slug": self.article.slug}),
            **self.bearer_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.favourite.count(), favourite)

    def test_unfavourite_twice_article(self) -> None:
        """test unfavourite an article"""
        unfavourite = self.article.unfavourite.count()
        response = self.client.patch(
            reverse("unfavourite", kwargs={"slug": self.article.slug}),
            **self.bearer_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.unfavourite.count(), unfavourite + 1)
        response = self.client.patch(
            reverse("unfavourite", kwargs={"slug": self.article.slug}),
            **self.bearer_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.unfavourite.count(), unfavourite)

    def test_favourite_article_unfavourite_article(self) -> None:
        """test favourite an article"""
        favourite = self.article.favourite.count()
        response = self.client.patch(
            reverse("favourite", kwargs={"slug": self.article.slug}),
            **self.bearer_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.favourite.count(), favourite + 1)
        unfavourite = self.article.unfavourite.count()
        response = self.client.patch(
            reverse("unfavourite", kwargs={"slug": self.article.slug}),
            **self.bearer_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.unfavourite.count(), unfavourite + 1)

    def test_unfavourite_article_favourite_article(self) -> None:
        """test unfavourite an article"""
        unfavourite = self.article.unfavourite.count()
        response = self.client.patch(
            reverse("unfavourite", kwargs={"slug": self.article.slug}),
            **self.bearer_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.unfavourite.count(), unfavourite + 1)
        favourite = self.article.favourite.count()
        response = self.client.patch(
            reverse("favourite", kwargs={"slug": self.article.slug}),
            **self.bearer_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.favourite.count(), favourite + 1)
