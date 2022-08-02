from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from PIL import Image

fake = Faker()


def sample_image() -> SimpleUploadedFile:
    image_file = BytesIO()
    image = Image.new("RGBA", size=(50, 50), color=(256, 0, 0))
    image.save(image_file, "png")
    image_file.seek(0)
    return SimpleUploadedFile(
        "tests.png", image_file.read(), content_type="image/png"
    )
