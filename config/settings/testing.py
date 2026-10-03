"""Fast, isolated settings for the Django test suite."""

# noinspection unused-imports
from .base import *

SECRET_KEY = "django-insecure-tests-only-do-not-use-in-production"
ALLOWED_HOSTS = ["test-server", "localhost", "127.0.0.1"]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]