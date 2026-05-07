from .base import *

DEBUG = False
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="").split(",")

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
