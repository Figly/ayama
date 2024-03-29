import logging.config as config

from .settings_base import *  # noqa

if not os.environ.get("ENVIRONMENT", False) or os.environ.get("ENVIRONMENT") in [
    "dev",
]:
    print(os.environ.get("ENVIRONMENT", False))
    TEMPLATES[0]["OPTIONS"].update({"debug": True})

    # Django Debug Toolbar
    INSTALLED_APPS += ("debug_toolbar",)

    # Additional middleware introduced by debug toolbar
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

    # Show thumbnail generation errors
    THUMBNAIL_DEBUG = True
    # Allow internal IPs for debugging
    INTERNAL_IPS = ["127.0.0.1", "0.0.0.1"]

    # Emails in sandbox mode
    SENDGRID_SANDBOX_MODE_IN_DEBUG = True
    SENDGRID_ECHO_TO_STDOUT = True

else:
    # Emails in sandbox mode
    SENDGRID_SANDBOX_MODE_IN_DEBUG = False
    SENDGRID_ECHO_TO_STDOUT = False

    # Cache the templates in memory for speed-up
    loaders = [
        (
            "django.template.loaders.cached.Loader",
            [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        )
    ]

    TEMPLATES[0]["OPTIONS"].update({"loaders": loaders})
    TEMPLATES[0].update({"APP_DIRS": False})

    # Setup static file serving
    STATIC_ROOT = os.path.join(Path(__file__).resolve().parent, "static/")

    # Configure static and media file access on GCS
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"

    STATICFILES_FINDERS = [
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
        "django.contrib.staticfiles.finders.DefaultStorageFinder",
        "django.contrib.staticfiles.finders.FileSystemFinder",
    ]

    if os.environ.get("ENVIRONMENT") != "production":
        GS_BUCKET_NAME = "ayama-staging-assets"
    else:
        GS_BUCKET_NAME = "ayama-production-production"

    STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    STATIC_URL = "https://storage.googleapis.com/ayama-staging-assets/"

    # static file serving credentials
    GS_ACCESS_KEY_ID = os.environ.get("GS_ACCESS_KEY_ID", None)
    GS_SECRET_ACCESS_KEY = os.environ.get("GS_SECRET_ACCESS_KEY", None)

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
                "filename": os.path.join(os.getenv("AYAMA_LOG_DIR", "."), "ayama.log"),
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
