from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

fake = Faker()
User = get_user_model()


class UserFollowingTest(TestCase):
    def setUp(self) -> None:
        self.password = fake.password()
        self.user_one = User.objects.create_user(
            username=fake.name(), email=fake.email(), password=self.password
        )
        self.user_two = User.objects.create_user(
            username=fake.name(), email=fake.email(), password=self.password
        )

    def test_get_followers(self) -> None:
        url = reverse("follow", kwargs={"pk": self.user_one.id})
        response = self.client.get(
            url,
            kwargs={"pk": self.user_one.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_no_followers(self) -> None:
        url = reverse("follow", kwargs={"pk": self.user_one.id})
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_follow_same_user(self) -> None:
        url = reverse("follow", kwargs={"pk": self.user_two.id})
        self.client.post(
            url,
            kwargs={"pk": self.user_two.id},
            format="json",
        )
        response = self.client.post(
            url,
            kwargs={"pk": self.user_two.id},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesMessage(
            PermissionDenied, "You cannot follow this user."
        )

    def test_user_unfollow(self) -> None:
        url = reverse("follow", kwargs={"pk": self.user_two.id})
        self.client.get(
            url,
            kwargs={"pk": self.user_two.id},
            format="json",
        )
        response = self.client.delete(
            url,
            kwargs={"pk": self.user_two.id},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaisesMessage(
            PermissionDenied, "you are no longer following this user"
        )
