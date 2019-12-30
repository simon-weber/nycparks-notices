import logging
import os

import django_heroku
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration, ignore_logger


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# env var expected for SECRET_KEY
DEBUG = False
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

SCHEME = 'https'
HOST = 'parks.simon.codes'
PORT = None
ALLOWED_HOSTS = []

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ignore the admin app wanting messages (which are disabled since they're replaced for caching)
SILENCED_SYSTEM_CHECKS = ["admin.E404", "admin.E406", "admin.E409"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "parkalerts.core",
    "bootstrap3",
    "django_extensions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "parkalerts.urls"

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
            ]
        },
    }
]

WSGI_APPLICATION = "parkalerts.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "US/Eastern"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = "/static/"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'INFO',
        'handlers': ['console_verbose'],
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s: %(asctime)s - %(name)s: %(message)s'
        },
        'withfile': {
            'format': '%(levelname)s: %(asctime)s - %(name)s (%(module)s:%(lineno)s): %(message)s'
        },
    },
    'handlers': {
        'console_simple': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'console_verbose': {
            'class': 'logging.StreamHandler',
            'formatter': 'withfile',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console_simple'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'WARNING'),
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console_simple'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'parkalerts': {
            'handlers': ['console_verbose'],
            'level': 'INFO',
            'propagate': False,
        },
        'newrelic': {
            'handlers': ['console_simple'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

EMAIL_BACKEND = 'django_ses.SESBackend'
DEFAULT_FROM_EMAIL = 'NYC Park Alerts <noreply@parks.simon.codes>'
ADMINS = (('Simon', 'simon@simonmweber.com'),)
SERVER_EMAIL = DEFAULT_FROM_EMAIL

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.WARNING,
)
ignore_logger("newrelic")
sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[
        DjangoIntegration(),
        sentry_logging,
    ],
)

django_heroku.settings(locals(), logging=False)

DATABASES['default']['ENGINE'] = 'django_db_geventpool.backends.postgresql_psycopg2'  # noqa: F821
DATABASES['default']['CONN_MAX_AGE'] = 0  # noqa: F821
DATABASES['default']['OPTIONS']['MAX_CONNS'] = 5  # noqa: F821
