from .settings import *  # noqa

SECRET_KEY = 'dev_secret_key'
DEBUG = True
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_BROWSER_XSS_FILTER = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
X_FRAME_OPTIONS = 'SAMEORIGIN'

SCHEME = 'http'
HOST = '127.0.0.1'
PORT = 8000

USE_X_FORWARDED_HOST = False
SECURE_PROXY_SSL_HEADER = None

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# disable sentry
sentry_sdk.init(dsn='')  # noqa: F405
