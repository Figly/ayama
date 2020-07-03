"""
Django settings for ayama project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import os
import socket
from pathlib import Path

from django.contrib import messages
from django.urls import reverse_lazy

DEBUG = os.getenv(
    "DEBUG", True
)  # Defaulting to true for dev purposes - should always be set in staging/prod

BASE_DIR = Path(__file__).resolve().parent.parent
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "media"),
)

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = "/media/"
STATIC_URL = "/static/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(BASE_DIR / "templates"),
            # insert more TEMPLATE_DIRS here
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

TEMPLATE_LOADERS = ("django.template.loaders.app_directories.load_template_source",)

SECRET_KEY = os.environ.get("SECRET_KEY", "notsosecretdevkey")

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "authtools",
    "crispy_forms",
    "easy_thumbnails",
    "profiles",
    "accounts",
    "calculator",
    "clients",
    "practises",
    "formtools",
    "comms",
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ayama.urls"

WSGI_APPLICATION = "ayama.wsgi.application"

if not os.environ.get("ENVIRONMENT", False):
    DATABASES = {
        "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.getenv("POSTGRES_DB", "ayama"),
            "USER": os.getenv("POSTGRES_USER", "postgres"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
            "HOST": os.getenv("AYAMA_POSTGRES_SERVICE_HOST", "ayama-postgres"),
            "PORT": os.getenv("AYAMA_POSTGRES_SERVICE_PORT", 5432),
        },
    }
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": [
                "redis://%s:%s"
                % (
                    os.getenv(
                        "REDIS_HOST",
                        os.getenv("AYAMA_REDIS_SERVICE_HOST", "ayama-redis"),
                    ),
                    os.getenv(
                        "REDIS_PORT", os.getenv("AYAMA_REDIS_SERVICE_PORT", 6379)
                    ),
                ),
            ],
            "OPTIONS": {
                "DB": 1,
                "PARSER_CLASS": "redis.connection.HiredisParser",
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "CONNECTION_POOL_CLASS": "redis.BlockingConnectionPool",
            },
        },
    }

# Email settings
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

HOSTNAME = socket.gethostname()

LANGUAGE_CODE = "en-za"
USE_I18N = True
USE_L10N = True

USE_TZ = True
TIME_ZONE = "Africa/Johannesburg"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Crispy Form Theme - Bootstrap 4
CRISPY_TEMPLATE_PACK = "bootstrap4"

MESSAGE_TAGS = {messages.ERROR: "danger"}

# Authentication Settings
AUTH_USER_MODEL = "practises.User"
LOGIN_REDIRECT_URL = reverse_lazy("profiles:show_self")
LOGIN_URL = reverse_lazy("accounts:login")

THUMBNAIL_EXTENSION = "png"

DATE_INPUT_FORMATS = ["%Y-%m-%d"]
