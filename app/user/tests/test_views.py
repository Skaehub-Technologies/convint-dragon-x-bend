from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status

from app.user.token import account_activation_token

User = get_user_model()


class ViewsTest(TestCase):
    """Testing views"""

    def setUp(self) -> None:
        self.test_user = User.objects.create_user(
            "testuser", "test@mail.com", "tester012"
        )
        self.create_url = reverse("register")

    # Testing UserView
    def test_create_user(self) -> None:
        data = {
            "username": "foobarata",
            "email": "foobar@example.com",
            "password": "somepassword",
        }

        response = self.client.post(self.create_url, data, format="json")

        self.assertNotEqual(response, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], str("foobarata"))  # type: ignore
        self.assertEqual(response.data["email"], str("foobar@example.com"))  # type: ignore
        self.assertFalse("password" in response.data)  # type: ignore

    def test_new_user_verification(self) -> None:
        new_user = User.objects.create_user(
            "humptydumpty", "humpty@gmail.com", "felldownthewall"
        )
        link = reverse(
            "email-verify",
            kwargs={
                "uidb64": urlsafe_base64_encode(force_bytes(new_user.pk)),
                "token": account_activation_token.make_token(new_user),
            },
        )
        resp = self.client.get(link)

        self.assertEqual(resp.status_code, 200)
