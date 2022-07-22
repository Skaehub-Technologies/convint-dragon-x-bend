from typing import Any
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from app.user.token import account_activation_token

from .mocks import test_user

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
    class UserFollowingTest(TestCase):
        def setUp(self) -> None:
            self.password = fake.password()
            self.user_one = User.objects.create_user(
                username=fake.name(),
                email=fake.email(),
                password=self.password,
            )
            self.user_two = User.objects.create_user(
                username=fake.name(),
                email=fake.email(),
                password=self.password,
            )

        def test_get_followers(self) -> None:
            url = reverse("following", kwargs={"id": self.user_one.id})
            response = self.client.get(
                url,
                kwargs={"id": self.user_one.id},
                format="json",
            )
            self.assertEqual(
                response.status_code, status.HTTP_401_UNAUTHORIZED
            )

        # def test_user_no_followers(self) -> None:
        #     url = reverse("following", kwargs={"id": self.user_one.id})
        #     response = self.client.post(url, format="json")
        #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # def test_user_cannot_follow_same_user(self) -> None:
        #     url = reverse("follow", kwargs={"id": self.user_two.id})
        #     self.client.post(
        #         url,
        #         kwargs={"id": self.user_two.id},
        #         format="json",
        #     )
        #     response = self.client.post(
        #         url,
        #         kwargs={"id": self.user_two.id},
        #         format="json",
        #     )

        #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        #     self.assertRaisesMessage(
        #         PermissionDenied, "You already following this user"
        #     )

        # def test_user_unfollow(self) -> None:
        #     url = reverse("unfollow", kwargs={"id": self.user_two.id})
        #     self.client.get(
        #         url,
        #         kwargs={"id": self.user_two.id},
        #         format="json",
        #     )
        #     response = self.client.delete(
        #         url,
        #         kwargs={"id": self.user_two.id},
        #         format="json",
        #     )

        #     self.assertEqual(response.status_code, status.HTTP_200_OK)
        #     self.assertRaisesMessage(
        #         PermissionDenied, "Successfully unfollowed"
        #     )
