import json
from typing import Any
from unittest.mock import patch

import cloudinary
from decouple import config
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from app.articles.models import Article
from app.user.models import Profile
from app.user.token import account_activation_token

from .mock import sample_data, sample_image
from .mocks import test_image, test_user

cloudinary.config(
    cloud_name="devowino",
    api_key=config("CLOUDINARY_API_KEY"),
    api_secret=config("API_SECRET"),
)


User = get_user_model()
fake = Faker()


class UserRegisterViewsTest(TestCase):
    """
    Test case for user registration views
    """

    user: Any

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(
            fake.name(), fake.email(), fake.password()
        )

    def setUp(self) -> None:
        self.create_url = reverse("register")

    def test_create_user(self) -> None:
        """
        Test can create user
        """
        data = {
            "username": fake.name(),
            "email": fake.email(),
            "password": fake.password(),
        }

        response = self.client.post(self.create_url, data, format="json")
        res_data = response.data  # type: ignore[attr-defined]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_data["username"], data["username"])
        self.assertEqual(res_data["email"], data["email"])
        self.assertTrue(len(mail.outbox) > 0)

    def test_new_user_verification(self) -> None:
        """
        Test verification of user
        """
        link = reverse(
            "email-verify",
            kwargs={
                "uidb64": urlsafe_base64_encode(force_bytes(self.user.pk)),
                "token": account_activation_token.make_token(self.user),
            },
        )

        resp = self.client.patch(link)

        self.assertEqual(resp.status_code, 200)

    def test_invalid_user_id(self) -> None:
        """
        Test invalid user id
        """
        link = reverse(
            "email-verify",
            kwargs={
                "uidb64": urlsafe_base64_encode(
                    force_bytes("7efcc181-9741-4911-bb0c-e5f670dda1e1")
                ),
                "token": account_activation_token.make_token(self.user),
            },
        )

        resp = self.client.patch(link)

        self.assertEqual(resp.status_code, 400)
        self.assertIn("Invalid user id", str(resp.data))  # type: ignore[attr-defined]

    def test_invalid_token(self) -> None:
        """
        Test cannot use invalid token
        """
        link = reverse(
            "email-verify",
            kwargs={
                "uidb64": urlsafe_base64_encode(force_bytes(self.user.pk)),
                "token": "rgtuj54647vhd",
            },
        )

        resp = self.client.patch(link)

        self.assertEqual(resp.status_code, 400)
        self.assertIn("Invalid or expired token", str(resp.data))  # type: ignore[attr-defined]


class TestProfileView(APITestCase):
    """
    Test for Profile Model view
    """

    def setUp(self) -> None:
        self.user_test = User.objects.create_user(**test_user)

        self.client = APIClient()

    @property
    def bearer_token(self) -> str:
        login_url = reverse("login")
        response = self.client.post(
            login_url,
            data={
                "email": test_user["email"],
                "password": test_user["password"],
            },
            format="json",
        )
        return response.data.get("access")  # type: ignore[no-any-return]

    @patch(
        "cloudinary.uploader.upload_resource", return_value=fake.image_url()
    )
    def test_profile_update(self, upload_resource: Any) -> None:
        """
        Test updating of profile by user
        """
        Profile.objects.create(user=self.user_test)
        data = {
            "bio": "Do I function",
            "image": test_image,
        }
        url = reverse("profile", kwargs={"user": self.user_test.id})
        self.client.defaults[
            "HTTP_AUTHORIZATION"
        ] = f"Bearer {self.bearer_token}"
        response = self.client.patch(
            url,
            data=encode_multipart(data=data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
            enctype="multipart/form-data",
        )

        self.assertTrue(upload_resource.called)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestArticleViews(APITestCase):
    """
    Tests for Article App views
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Data to be used in the tests
        """
        super().setUpClass()
        cls.password = fake.password()  # type: ignore[attr-defined]
        cls.client = APIClient()
        cls.user = User.objects.create_user(  # type: ignore[attr-defined]
            username=fake.name(), email=fake.email(), password=cls.password  # type: ignore[attr-defined]
        )
        cls.article = Article.objects.create(  # type: ignore[attr-defined]
            title=fake.name(),
            description=fake.text(),
            body=fake.text(),
            image=sample_image(),
            taglist=f'["{fake.word()}", "{fake.word()}"]',
            favourited=False,
            favouritesCount=0,
            author=cls.user,  # type: ignore[attr-defined]
        )
        cls.data = {  # type: ignore[attr-defined]
            "title": fake.texts(nb_texts=2),
            "description": fake.paragraph(nb_sentences=3),
            "body": fake.paragraph(nb_sentences=20),
            "image": sample_image(),
            "taglist": f'["{fake.word()}", "{fake.word()}"]',
            "favourited": False,
            "favouritesCount": 0,
        }

    @property
    def bearer_token(self) -> dict:
        """
        Authentication function
        """
        login_url = reverse("login")
        response = self.client.post(
            login_url,
            data={"email": self.user.email, "password": self.password},  # type: ignore[attr-defined]
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
            data=encode_multipart(data=self.data, boundary=BOUNDARY),  # type: ignore[attr-defined]
            content_type=MULTIPART_CONTENT,
            enctype="multipart/form-data",
            **self.bearer_token,
        )
        self.assertFalse(upload_resource.called)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Article.objects.count(), count)

    def test_create_article_without_article(self) -> None:
        """
        Test when an article is created without an article
        """
        data = sample_data()
        data.pop("title")
        count = Article.objects.count()
        response = self.client.post(
            reverse("create"),
            data=encode_multipart(data=data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
            enctype="multipart/form-data",
            **self.bearer_token,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.dumps(response.data),
            '{"title": ["This field is required."]}',
        )
        self.assertEqual(Article.objects.count(), count)

    def test_delete_article(self) -> None:
        """
        Test deletion of an article by the author
        """
        count = Article.objects.count()
        response = self.client.delete(
            reverse("article-delete", kwargs={"slug": self.article.slug}),  # type: ignore[attr-defined]
            **self.bearer_token,
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), count - 1)

    def test_delete_article_without_authentication(self) -> None:
        """
        Test deletion of an article by a foreign user
        """
        count = Article.objects.count()
        response = self.client.delete(
            reverse("article-delete", kwargs={"slug": self.article.slug})  # type: ignore[attr-defined]
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Article.objects.count(), count)
        self.assertEqual(
            json.loads(response.content).get("detail"),
            "Authentication credentials were not provided.",
        )
