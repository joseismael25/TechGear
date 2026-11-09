"""Configuración de Django para el portal web TechGear."""
import os
from pathlib import Path

from dotenv import load_dotenv
from django.contrib.messages import constants as message_constants

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() in {"true", "1", "yes"}

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "").strip()

if not SECRET_KEY:
    if not DEBUG:
        raise RuntimeError(
            "Configura DJANGO_SECRET_KEY en las variables de entorno."
        )
    SECRET_KEY = "django-insecure-techgear-local-development-only-change-this-key"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        "127.0.0.1,localhost"
    ).split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "store",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "techgear_web.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ],
    },
}]

WSGI_APPLICATION = "techgear_web.wsgi.application"
ASGI_APPLICATION = "techgear_web.asgi.application"

# Base de datos local de Django.
# MongoDB continúa siendo administrada por FastAPI.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "OPTIONS": {"timeout": 20},
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]

LANGUAGE_CODE = "es"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
).rstrip("/")

MESSAGE_TAGS = {
    message_constants.ERROR: "danger"
}

# Sesiones firmadas: Django no necesita escribir las sesiones en SQLite.
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

SESSION_COOKIE_AGE = 60 * 60
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

CSRF_COOKIE_SAMESITE = "Lax"

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"

if not DEBUG:
    SESSION_COOKIE_SECURE = os.getenv(
        "DJANGO_SECURE_COOKIES",
        "True"
    ).lower() in {"true", "1", "yes"}

    CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE