import os
import dj_database_url
from corsheaders.defaults import default_headers
from datetime import timedelta
from decouple import config

from .env import ABS_PATH, ENV_BOOL, ENV_INT, ENV_LIST, ENV_STR, BASE_DIR

DEBUG = ENV_BOOL("DEBUG", False)
SECRET_KEY = ENV_STR("SECRET_KEY", "secret" if DEBUG else "")
# ALLOWED_HOSTS = ENV_LIST("ALLOWED_HOSTS", ",", ["*"] if DEBUG else [])
ALLOWED_HOSTS = ['100.64.222.154','127.0.0.1','localhost']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "daphne", 
    "channels",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "rest_framework_simplejwt",
    "core.apps.CoreConfig",
    "users.apps.UsersConfig",
    "chat.apps.ChatConfig",
    "openapi.apps.OpenAPIConfig",
    "sphereEngine.apps.SphereEngineConfig",
    "drf_spectacular",
    "django_countries",
    "phonenumber_field",
    "django_extensions",
    "cities_light",
    "django_celery_results",
    
]

ASGI_APPLICATION='project.settings.asgi.application'

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
]


ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "frontend/build")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "project.wsgi.application"

DATABASES = {"default": dj_database_url.config()}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa: E501
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

# allauth settings
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "none"
LOGOUT_ON_PASSWORD_CHANGE = False
LOGIN_REDIRECT_URL = "chat-page"
# LOGIN_REDIRECT_URL = "/"

REST_AUTH = {
    "SESSION_LOGIN": False,
}
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

SITE_ID = 1

# static and media
STATIC_URL = ENV_STR("STATIC_URL", "/static/")
STATIC_ROOT = ENV_STR("STATIC_ROOT", ABS_PATH("static"))

MEDIA_URL = ENV_STR("MEDIA_URL", "/media/")
MEDIA_ROOT = ABS_PATH(ENV_STR("MEDIA_ROOT", "media"))
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = ENV_STR("EMAIL_HOST", "localhost")
EMAIL_HOST_USER = ENV_STR("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = ENV_STR("EMAIL_HOST_PASSWORD", "")
EMAIL_PORT = ENV_INT("EMAIL_PORT", 25)
EMAIL_USE_TLS = ENV_BOOL("EMAIL_USE_TLS", False)
SERVER_EMAIL = ENV_STR("SERVER_EMAIL", "webmaster@localhost")
DEFAULT_FROM_EMAIL = ENV_STR("DEFAULT_FROM_EMAIL", SERVER_EMAIL)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),

    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# log to console, assume the supervisor/system runner will take care of the logs
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "null": {"level": "DEBUG", "class": "logging.NullHandler"},
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": ENV_STR("LOG_LEVEL", "INFO"),
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
    },
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_SUBJECT_PREFIX = '[Django]'


DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
EMAIL_SUBJECT_PREFIX = '[Django]'

# Sphere Engine Configuration
SPHERE_ENGINE_COMPILER_ACCESS_TOKEN = '409e09b9909c4e230776c63c69e09469'
SPHERE_ENGINE_PROBLEMS_ACCESS_TOKEN = '763cea7fd8efbf89c879314221d8c2ab'
SPHERE_ENGINE_COMPILER_ENDPOINT = '203deddf.compilers.sphere-engine.com'
SPHERE_ENGINE_PROBLEMS_ENDPOINT = '203deddf.problems.sphere-engine.com'

PHONENUMBER_DEFAULT_REGION = "NP"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=90),
    "UPDATE_LAST_LOGIN": True,
    "TOKEN_OBTAIN_SERIALIZER": "core.serializers.CustomTokenObtainPairSerializer",
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = default_headers + ("content-disposition",)

if ENV_BOOL("USE_X_FORWARDED_PROTO"):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = ENV_BOOL("USE_X_FORWARDED_HOST")
USE_X_FORWARDED_PORT = ENV_BOOL("USE_X_FORWARDED_PORT")

LOGOUT_REDIRECT_URL="login-user"

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/1'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

SPECTACULAR_SETTINGS = {
    "TITLE": "CodeConnect System API",
    "DESCRIPTION": "API for Connect Connect API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
