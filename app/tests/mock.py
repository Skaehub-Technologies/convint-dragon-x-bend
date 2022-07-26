from io import BytesIO

import cloudinary
from decouple import config
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from PIL import Image

cloudinary.config(
    cloud_name="devowino",
    api_key=config("CLOUDINARY_API_KEY"),
    api_secret=config("API_SECRET"),
)

fake = Faker()


def sample_image() -> SimpleUploadedFile:
    image_file = BytesIO()
    image = Image.new("RGBA", size=(50, 50), color=(256, 0, 0))
    image.save(image_file, "png")
    image_file.seek(0)
    return SimpleUploadedFile(
        "tests.png", image_file.read(), content_type="image/png"
    )


def sample_data() -> dict:
    return {
        "title": fake.name(),
        "description": fake.text(),
        "body": fake.text(),
        "image": sample_image(),
        "taglist": f'["{fake.word()}", "{fake.word()}"]',
        "favourited": False,
        "favouritesCount": 0,
    }
