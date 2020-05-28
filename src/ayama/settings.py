import logging.config as config

from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG") == "True"

TEMPLATES[0]["OPTIONS"].update({"debug": True})

# Less strict password authentication and validation
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
# Django Debug Toolbar
INSTALLED_APPS += ("debug_toolbar",)

# Additional middleware introduced by debug toolbar
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

# Show emails to console in DEBUG mode
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Show thumbnail generation errors
THUMBNAIL_DEBUG = True

# Allow internal IPs for debugging
INTERNAL_IPS = ["127.0.0.1", "0.0.0.1"]

LOGGING_CONFIG = None
LOG_LEVEL = os.environ.get("AYAMA_LOG_LEVEL", "warning").upper()
config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
            },
            "detailed": {
                "format": "%(asctime)s %(module)-17s line:%(lineno)-4d %(levelname)-8s %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "level": LOG_LEVEL,
                "class": "logging.FileHandler",
                "filename": os.path.join(
                    os.getenv("AYAMA_LOG_DIR", "."), "ayama.log"
                ),
                "formatter": "detailed",
            },
        },
        "loggers": {
            "": {"level": "WARNING", "handlers": ["console", "file"]},
            "ayama": {
                "level": LOG_LEVEL,
                "handlers": ["console", "file"],
                "propagate": False,
            },
        },
    }
)
