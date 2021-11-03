"""
Base settings to build other settings files upon.
"""
from pathlib import Path

import environ

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# hasker/
APPS_DIR = ROOT_DIR / "hasker"
env = environ.Env()

READ_DOT_ENV_FILE = True
if READ_DOT_ENV_FILE:
    env.read_env(str(ROOT_DIR / ".env"))

DEBUG = env.bool("DJANGO_DEBUG", False)
TIME_ZONE = "Europe/Moscow"
LANGUAGE_CODE = "en-us"
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = [str(ROOT_DIR / "locale")]

DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.forms",
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    "rest_framework",
    "rest_framework.authtoken",
]

LOCAL_APPS = [
    "hasker.users.apps.UsersConfig",
    'hasker.qa'
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIGRATION_MODULES = {"sites": "hasker.contrib.sites.migrations"}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "qa:home"
LOGIN_URL = "account_login"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STATIC_ROOT = str(ROOT_DIR / "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(APPS_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_ROOT = str(APPS_DIR / "media")
MEDIA_URL = "/media/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "OPTIONS": {
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "hasker.utils.context_processors.settings_context",
            ],
        },
    }
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

CRISPY_TEMPLATE_PACK = "bootstrap4"

FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'Hass from Hasker <hasker@hasker.com>'

EMAIL_TIMEOUT = 5

ADMIN_URL = "admin/"
ADMINS = [("""Aleksandr Sergeenko""", "asergeenko@gmail.com")]
MANAGERS = ADMINS

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}
