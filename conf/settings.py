import json
import os
import sys

from django.urls import reverse_lazy
from environ import Env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_FILE = os.path.join(BASE_DIR, ".env")
if os.path.exists(ENV_FILE):
    Env.read_env(ENV_FILE)

env = Env(
    ALLOWED_HOSTS=(str, ""),
    DEBUG=(bool, False),
    LOG_LEVEL=(str, "INFO"),
    SECURE_HSTS_ENABLED=(bool, False),
    CSP_DEFAULT_SRC=(list, []),
    CSP_STYLE_SRC=(list, []),
    CSP_SCRIPT_SRC=(list, []),
    CSP_FONT_SRC=(list, []),
    CSP_IMG_SRC=(list, []),
    CSP_FRAME_SRC=(list, []),
    CSP_CONNECT_SRC=(list, []),
    CSP_INCLUDE_NONCE_IN=(list, []),
    CSP_REPORT_ONLY=(bool, True),
    HAWK_AUTHENTICATION_ENABLED=(bool, False),
)


DEBUG_PROPAGATE_EXCEPTIONS = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = json.loads(env("ALLOWED_HOSTS")) if env("ALLOWED_HOSTS") else []

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sass_processor",
    "django.contrib.humanize",
    "core.apps.CoreConfig",
    "svg",
    "lite_forms",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "conf.middleware.LoggingMiddleware",
    "conf.middleware.ProtectAllViewsMiddleware",
    "conf.middleware.UploadFailedMiddleware",
    "django.middleware.gzip.GZipMiddleware",
]

ROOT_URLCONF = "conf.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "conf.context_processors.export_vars",
            ],
            "builtins": ["core.builtins.custom_tags"],
        },
    },
]

# Authbroker config
AUTHBROKER_URL = env("AUTHBROKER_URL")
AUTHBROKER_CLIENT_ID = env("AUTHBROKER_CLIENT_ID")
AUTHBROKER_CLIENT_SECRET = env("AUTHBROKER_CLIENT_SECRET")

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "auth.backends.AuthbrokerBackend",
]

HAWK_AUTHENTICATION_ENABLED = env("HAWK_AUTHENTICATION_ENABLED")
HAWK_RECEIVER_NONCE_EXPIRY_SECONDS = 60

LOGIN_URL = reverse_lazy("auth:login")
LOGIN_REDIRECT_URL = reverse_lazy("core:home")
LOGOUT_URL = AUTHBROKER_URL + "/sso/accounts/logout/?next="
AUTH_USER_MODEL = "core.User"

WSGI_APPLICATION = "conf.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

DATA_DIR = os.path.dirname(BASE_DIR)

SVG_DIRS = [
    os.path.join(BASE_DIR, "assets/images"),
    os.path.join(BASE_DIR, "assets/shared/lite-frontend/assets/images"),
]

STATIC_URL = "/assets/"
STATIC_ROOT = os.path.join(DATA_DIR, "assets")

SASS_ROOT = os.path.join(BASE_DIR, "assets")
SASS_PROCESSOR_ROOT = SASS_ROOT

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "assets"),
    os.path.join(BASE_DIR, "assets/shared/node_modules/govuk-frontend/govuk/"),
    os.path.join(BASE_DIR, "assets/shared/node_modules/govuk-frontend/govuk/assets/"),
    os.path.join(BASE_DIR, "assets/shared/lite-frontend/"),
)

SASS_PROCESSOR_INCLUDE_DIRS = (os.path.join(BASE_DIR, "assets"), SASS_ROOT)

SASS_OUTPUT_STYLE = "compressed"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
)

# Cache static files
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

SASS_PROCESSOR_ENABLED = True


# File Upload
# https://github.com/uktrade/s3chunkuploader
S3_DOCUMENT_ROOT_DIRECTORY = ""
S3_APPEND_DATETIME_ON_UPLOAD = True
S3_PREFIX_QUERY_PARAM_NAME = ""
S3_DOWNLOAD_LINK_EXPIRY_SECONDS = 180
STREAMING_CHUNK_SIZE = 8192
S3_MIN_PART_SIZE = 5 * 1024 * 1024
MAX_UPLOAD_SIZE = 50 * 1024 * 1024

# AWS
VCAP_SERVICES = env.json("VCAP_SERVICES", {})

if VCAP_SERVICES:
    if "aws-s3-bucket" not in VCAP_SERVICES:
        raise Exception("S3 Bucket not bound to environment")

    aws_credentials = VCAP_SERVICES["aws-s3-bucket"][0]["credentials"]
    AWS_ACCESS_KEY_ID = aws_credentials["aws_access_key_id"]
    AWS_SECRET_ACCESS_KEY = aws_credentials["aws_secret_access_key"]
    AWS_REGION = aws_credentials["aws_region"]
    AWS_STORAGE_BUCKET_NAME = aws_credentials["bucket_name"]
else:
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = env("AWS_REGION")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if "test" in sys.argv:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "mydatabase"}}
else:
    DATABASES = {"default": env.db()}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "(asctime)(levelname)(message)(filename)(lineno)(threadName)(name)(thread)(created)(process)(processName)(relativeCreated)(module)(funcName)(levelno)(msecs)(pathname)",  # noqa
        },
    },
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "json",},},
    "loggers": {"": {"handlers": ["console"], "level": env("LOG_LEVEL").upper(),},},
}

# Security settings

SECURE_HSTS_ENABLED = env("SECURE_HSTS_ENABLED")
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 365 if SECURE_HSTS_ENABLED else None  # 1 year
SECURE_BROWSER_XSS_FILTER = not DEBUG

SESSION_COOKIE_SECURE = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = not DEBUG

CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = not DEBUG

X_FRAME_OPTIONS = "SAMEORIGIN"

# Content Security Policy
CSP_DEFAULT_SRC = env("CSP_DEFAULT_SRC")
CSP_STYLE_SRC = env("CSP_STYLE_SRC")
CSP_SCRIPT_SRC = env("CSP_SCRIPT_SRC")
CSP_FONT_SRC = env("CSP_FONT_SRC")
CSP_IMG_SRC = env("CSP_IMG_SRC")
CSP_FRAME_SRC = env("CSP_FRAME_SRC")
CSP_CONNECT_SRC = env("CSP_CONNECT_SRC")
CSP_INCLUDE_NONCE_IN = env("CSP_INCLUDE_NONCE_IN")
CSP_REPORT_ONLY = env("CSP_REPORT_ONLY")
