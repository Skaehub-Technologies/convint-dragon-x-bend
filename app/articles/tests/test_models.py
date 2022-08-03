from django.test import TestCase
from django.utils.text import slugify
from faker import Faker

from app.articles.models import Article, Tag

fake = Faker()


class TestArticleModels(TestCase):
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
        """
        Test if an article can be accessed using its title once its created
        """
        article = Article.objects.create(**self.data)
        self.assertEqual(str(article), article.title)

    def test_slug_article(self) -> None:
        """
        Test generation of a slug once an article is created
        """
        article = Article.objects.create(**self.data)
        self.assertEqual(
            article.slug, slugify(f"{article.title}-{article.post_id}")
        )


class TestTagModel(TestCase):
    """
    Testing Tag Model
    """

    def test_tag(self) -> None:
        """
        Test if a profile returns the username of the user
        """
        tags = Tag.objects.create(
            name=fake.word(),
        )

        self.assertEqual(str(tags), tags.name)
