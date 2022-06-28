from django.contrib.auth import get_user_model
from django.test import TestCase

from app.user.models import Profile

User = get_user_model()


class ImageUploadTest(TestCase):
    def test_get_image(self):  # type: ignore
        user = User.objects.create(
            username="bearhands",
            email="bear@gmail.com",
            password="bearpassword",
        )
        data = Profile.objects.create(
            image="images/sample.jpg", bio="Hello mellow", user_id=user.id
        )
        response = self.client.get(data.image)

        self.assertNotEqual(response, "sample.jpg")
