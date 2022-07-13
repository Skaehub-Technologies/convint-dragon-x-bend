from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from faker import Faker
from rest_framework import status

fake = Faker()
User = get_user_model()


class TestPasswordReset(TestCase):
    testuser: dict
    user: Any

    @classmethod
    def setUpClass(cls) -> None:
        cls.testuser = {
            "username": fake.user_name(),
            "email": fake.email(),
            "password": fake.password(),
        }
        cls.user = User.objects.create_user(**cls.testuser)
        return super().setUpClass()

    def test_password_reset_request(self) -> None:
        url = reverse("password-reset")
        data = {"email": self.testuser["email"]}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)

    def test_password_reset_none_existing_email(self) -> None:
        url = reverse("password-reset")
        data = {"email": fake.email()}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 0)

    def test_password_reset_no_email(self) -> None:
        url = reverse("password-reset")
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "This field may not be null", str(response.data["email"])  # type: ignore[attr-defined]
        )

    def test_verify_password_reset_token(self) -> None:
        token = PasswordResetTokenGenerator().make_token(self.user)
        encoded_pk = urlsafe_base64_encode(force_bytes(self.user.pk))
        reset_url = reverse(
            "verify-password-reset",
            kwargs={"encoded_pk": encoded_pk, "token": token},
        )
        response = self.client.post(
            reset_url, data={"password": fake.password()}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_password_reset_wrong_token(self) -> None:
        encoded_pk = urlsafe_base64_encode(force_bytes(self.user.pk))
        reset_url = reverse(
            "verify-password-reset",
            kwargs={"encoded_pk": encoded_pk, "token": "token"},
        )

        response = self.client.post(
            reset_url, data={"password": "mypassword"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "The reset token is invalid", str(response.data["detail"])  # type: ignore[attr-defined]
        )

    def test_verify_password_reset_wrong_encoded_pk(self) -> None:
        reset_url = reverse(
            "verify-password-reset",
            kwargs={"encoded_pk": "encoded_pk", "token": "token"},
        )

        response = self.client.post(
            reset_url, data={"password": "mypassword"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "The encoded_pk is invalid", str(response.data["detail"])  # type: ignore[attr-defined]
        )

    def test_invalid_user_id(self) -> None:

        reset_url = reverse(
            "verify-password-reset",
            kwargs={
                "encoded_pk": "encoded_pk",
                "token": "token",
            },
        )
        resp = self.client.post(reset_url)
        self.assertEqual(resp.status_code, 400)
        self.assertIn("This field is required", str(resp.data))  # type: ignore[attr-defined]
