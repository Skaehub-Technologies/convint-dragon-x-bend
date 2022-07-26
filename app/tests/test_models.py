from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.text import slugify
from faker import Faker

from app.articles.models import Article
from app.user.models import Profile

User = get_user_model()
fake = Faker()


class TestUserModel(TestCase):
    """Testing models"""

    # Testing user
    def test_create_user(self) -> None:
        user = User.objects.create_user(
            username="ndovu", email="ndovu@test.com", password="wild"
        )

        self.assertEqual(user.email, "ndovu@test.com")
        self.assertEqual(user.username, "ndovu")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_verified)

    def test_user_username_errors(self) -> None:
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username="", email="tembo@gmail.com", password="nice"
            )

    def test_user_email_errors(self) -> None:
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username="tembo", email="", password="wild"
            )

    def test_user_is_active(self) -> None:
        user = User.objects.create_user(
            username="tembo",
            email="tembo@gmail.com",
            is_active=True,
            password="wild",
        )

        self.assertEqual(user.email, "tembo@gmail.com")
        self.assertIsNot(user.username, "tembo1")
        self.assertEqual(user.is_active, True)

    def test_user_is_staff(self) -> None:
        user = User.objects.create_user(
            username="tembo",
            email="tembo@gmail.com",
            password="wild",
            is_staff=True,
        )

        self.assertEqual(user.is_staff, True)
        self.assertTrue(user.is_staff)

    def test_user_is_verified(self) -> None:
        user = User.objects.create_user(
            username="tembo",
            email="tembo@gmail.com",
            password="wild",
            is_verified=True,
        )

        self.assertIsNot(user.is_verified, False)
        self.assertTrue(user.is_verified)

    # Testing superuser model
    def test_create_superuser(self) -> None:
        user = User.objects.create_superuser(
            username="tembo",
            email="testsuperuser@test.com",
            password="helloworld",
        )

        self.assertIsInstance(user, User)
        self.assertEqual(user.email, "testsuperuser@test.com")
        self.assertEqual(user.username, "tembo")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_verified)

    def test_superuser_password_error(self) -> None:
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username="tembo", email="testsuperuser@test.com", password=""
            )

    def test_superuser_staff_error(self) -> None:
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username="tembo",
                email="testsuperuser@test.com",
                password="hello",
                is_staff=False,
            )

    def test_superuser_error(self) -> None:
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username="tembo",
                email="testsuperuser@test.com",
                password="hello",
                is_staff=True,
                is_superuser=False,
            )


class TestProfileModel(TestCase):
    """
    Testing profile
    """

    def test_profile(self) -> None:
        user = User.objects.create_user(
            username=fake.name(),
            email=fake.email(),
            password=fake.password(),
        )
        profile = Profile.objects.create(user=user)

        self.assertEqual(str(profile), user.username)


class TestArticleViews(TestCase):
    """
    Testing Articles Model
    """

    def setUp(self) -> None:
        self.data = {
            "title": fake.name(),
            "description": fake.text(),
            "body": fake.text(),
            "image": fake.image_url(),
            "favourited": False,
            "favouritesCount": 0,
        }

    def test_create_article(self) -> None:
        """
        Test creation of new article
        """
        article = Article.objects.create(**self.data)
        self.assertEqual(article.title, self.data["title"])
        self.assertEqual(article.description, self.data["description"])
        self.assertEqual(article.body, self.data["body"])
        self.assertEqual(article.image, self.data["image"])
        self.assertEqual(article.favourited, self.data["favourited"])
        self.assertEqual(article.favouritesCount, self.data["favouritesCount"])

    def test_str_article(self) -> None:
        article = Article.objects.create(**self.data)
        self.assertEqual(str(article), article.title)

    def test_slug_article(self) -> None:
        article = Article.objects.create(**self.data)
        self.assertEqual(
            article.slug, slugify(f"{article.title}-{article.article_id}")
        )
