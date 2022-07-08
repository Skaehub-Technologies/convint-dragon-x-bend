from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from faker import Faker
from rest_framework import status

from app.user.token import account_activation_token

User = get_user_model()
fake = Faker()


class UserRegisterViewsTest(TestCase):
    """Testing views"""

    def setUp(self) -> None:
        self.test_user = User.objects.create_user(
            fake.name(), fake.email(), fake.password()
        )
        self.create_url = reverse("register")

    def test_create_user(self) -> None:
        """Testing UserView"""
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

    def test_new_user_verification(self) -> None:
        new_user = User.objects.create_user(
            fake.name(), fake.email(), fake.password()
        )
        link = reverse(
            "email-verify",
            kwargs={
                "uidb64": urlsafe_base64_encode(force_bytes(new_user.pk)),
                "token": account_activation_token.make_token(new_user),
            },
        )

        resp = self.client.patch(link)

        self.assertEqual(resp.status_code, 200)
