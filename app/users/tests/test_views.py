from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from faker import Faker
from rest_framework import status

from app.users.views import PasswordReset, ResetPasswordAPI

password_reset = PasswordReset.as_view()
reset_password_api = ResetPasswordAPI.as_view()
fake = Faker()
User = get_user_model()


class PasswordResetTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username=fake.name(), email=fake.email(), password=fake.password()
        )

    def test_password_reset_request(self) -> None:
        url = reverse("request-password-reset")
        data = {"email": fake.email()}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_no_email(self) -> None:
        factory = RequestFactory()
        url = reverse("request-password-reset")
        request = factory.post(url, format="json")
        response = password_reset(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_password_reset_email(self) -> None:
        url = reverse("request-password-reset")
        data = {"email": fake.email()}
        response = self.client.post(url, data, format="json")
        self.assertEqual(
            response.data,  # type: ignore[attr-defined]
            {"message": "check your email for password reset link"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_token(self) -> None:
        token = PasswordResetTokenGenerator().make_token(self.user)
        encoded_pk = urlsafe_base64_encode(force_bytes(self.user.pk))
        reset_url = reverse(
            "reset-password", kwargs={"encoded_pk": encoded_pk, "token": token}
        )
        response = self.client.post(
            reset_url, data={"password": fake.password()}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_password_reset_wrong_token(self) -> None:
        encoded_pk = urlsafe_base64_encode(force_bytes(self.user.pk))
        reset_url = reverse(
            "reset-password",
            kwargs={"encoded_pk": encoded_pk, "token": "token"},
        )

        response = self.client.post(
            reset_url, data={"password": "mypassword"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "The reset token is invalid", str(response.data["detail"])  # type: ignore[attr-defined]
        )
