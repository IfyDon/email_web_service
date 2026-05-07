from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]
SECRET_KEY = config("SECRET_KEY", default="dev-insecure-key")

INSTALLED_APPS += [
    "django_extensions",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
