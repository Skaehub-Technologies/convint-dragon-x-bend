from speaksfer.settings.base import ALLOWED_HOSTS

DEBUG = True

ALLOWED_HOSTS += [
    ".herokuapp.com",
    "http://localhost:3000",
    "localhost",
    "127.0.0.1",
]
