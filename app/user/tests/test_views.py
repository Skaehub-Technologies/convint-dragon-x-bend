from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

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
