from speaksfer.settings.base import ALLOWED_HOSTS

ALLOWED_HOSTS += [
    "https://speaksfer-bend.herokuapp.com/",
    "http://localhost:3000",
    "localhost",
    "127.0.0.1",
]

DEBUG = True
