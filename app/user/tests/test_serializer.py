# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from faker import Faker


# User = get_user_model()
# fake = Faker()


# class ImageUploadTest(TestCase):
#     def test_get_image(self) -> None:
#         user = User.objects.create(
#             username=fake.name(),
#             email=fake.email(),
#             password=fake.password(),
#         )
#         data = Profile.objects.create(
#             image="images/sample.jpg", bio="Hello mellow", user_id=user.id
#         )
#         response = self.client.get(data.image)

#         self.assertNotEqual(response, "sample.jpg")
