import importlib.util
from pathlib import Path

from environs import Env


env = Env()

debug_toolbar = importlib.util.find_spec("debug_toolbar")
found_debug_toolbar = debug_toolbar is not None

HTTP_HOST = env.str("HTTP_HOST", "0.0.0.0")
HTTP_PORT = env.int("HTTP_PORT", 8000)

SENTRY_DSN = env.str("SENTRY_DSN", default="")

BUILD_VERSION = env.str("BUILD_VERSION", default="")
NAMESPACE = env.str("NAMESPACE", default="")

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-192t*c8w9b=xsla^p+q@!6n%*_2!dfuwsr+i$lkuy_c02ii1@("

DEBUG = env.bool("DEBUG", True)

IS_MIGRATION_JOB_ENV = env.bool("IS_MIGRATION_JOB_ENV", default=False)

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "apps.consumer",
    "apps.core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
    ),
}

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

DB_PASSWORD = env.str("POSTGRES_PASSWORD", "postgres")

if IS_MIGRATION_JOB_ENV:
    DB_PASSWORD = env.str("MIGRATION_POSTGRES_PASSWORD", "postgres")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": env.str("POSTGRES_HOST", "localhost"),
        "PORT": env.str("POSTGRES_PORT", "5432"),
        "NAME": env.str("POSTGRES_DB", "postgres"),
        "USER": env.str("POSTGRES_USER", "postgres"),
        "PASSWORD": DB_PASSWORD,
        "OPTIONS": {
            "target_session_attrs": "read-write",
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

HTTP_REQUEST_CONNECT_TIMEOUT_SECONDS = env.int("HTTP_REQUEST_CONNECT_TIMEOUT_SECONDS", 1)
HTTP_REQUEST_READ_TIMEOUT_SECONDS = env.int("HTTP_REQUEST_READ_TIMEOUT_SECONDS", 5)

STATISTIC_URL = "https://statistics-api.wildberries.ru"
SUPPLIERS_URL = "https://suppliers-api.wildberries.ru"

API_KEY = "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwNjE3djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTczNTYyNTE5NSwiaWQiOiIyZWJmMmFiOS1lOTZlLTQ0ZmItODBiZi1hNGU5ZmZjMmUwOTkiLCJpaWQiOjE4NjMyMTQ3LCJvaWQiOjc0MzA3NCwicyI6MTA3Mzc0MTg3NCwic2lkIjoiNzdhNTFkYjMtNDcxYS00M2M0LTgxNzktZDNmM2M4MGVlYWZlIiwidCI6ZmFsc2UsInVpZCI6MTg2MzIxNDd9.vrC9ydy1kerVsxf8XPSlOxQNDdlSLtnHluu4sqoMVSYYnEXlZl71wIBPjASJroHtKGt6oEb2dNLdWrAh8Hbz9A"
