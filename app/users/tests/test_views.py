from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status

from app.users.views import PasswordReset, ResetPasswordAPI

User = get_user_model()


class PasswordResetTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="chrisnemwel",
            email="chrisnemwel@gmail.com",
            password="secretpassword",
        )

    def test_password_reset_email(self) -> None:
        url = reverse("request-password-reset")
        factory = RequestFactory()
        request = factory.post(url, {"email": self.user.email}, format="json")
        response = PasswordReset.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_password_reset(self) -> None:
        url = reverse("request-password-reset")
        data = {"email": "chrisnemwel@gmail.com", "password": "secretpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_token(self) -> None:
        factory = RequestFactory()
        encoded_pk = urlsafe_base64_encode(force_bytes(self.user.pk))
        url = reverse(
            "reset-password", kwargs={"encoded_pk": encoded_pk, "token": None}
        )
        request = factory.patch(url)
        response = ResetPasswordAPI.as_view()(
            request, encoded_pk=encoded_pk, token=None
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
