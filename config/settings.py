"""
Django settings for Sendji_004 project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import json
import logging

import redis

from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv


load_dotenv(dotenv_path=".env")
logging.basicConfig(format="[%(asctime)s] | %(levelname)s: %(message)s", level=logging.INFO, datefmt='%m.%d.%Y %H:%M:%S')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DOC_SECRET_KEY", os.environ["SECRET_KEY"])

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv("DOC_DEBUG", os.environ["DEBUG"])) 

# allowed hosts
# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = json.loads(os.getenv("DOC_ALLOWED_HOSTS", os.environ["ALLOWED_HOSTS"]))

CORS_ALLOWED_ORIGINS = json.loads(os.getenv("DOC_CORS_ALLOWED_ORIGINS", os.environ["CORS_ALLOWED_ORIGINS"]))
CORS_ORIGIN_ALLOW_ALL = bool(os.getenv("DOC_CORS_ORIGIN_ALLOW_ALL", os.environ["CORS_ORIGIN_ALLOW_ALL"]))

# Application definition
INSTALLED_APPS = [
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'debug_toolbar',
    'django.contrib.humanize',
    'corsheaders',

    # OAuth2
    "social_django",

    # OpenAPI
    'drf_yasg', # It's working with DRF API

    # apps
    'src.main.apps.MainConfig',
    'src.users.apps.UsersConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # OAuth2
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
            'string_if_invalid': ''
        },
    },
]

# WSGI_APPLICATION = 'config.wsgi.application'

ASGI_APPLICATION = "config.asgi.application"


# Channels settings
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.environ.get('DOC_HOST_CL', os.environ['HOST_DB']), 6379)],
            "group_expiry": 10800,
        },
    },
}

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DOC_ENGINE', os.environ['ENGINE_DB']),
        'NAME': os.environ.get('DOC_NAME', os.environ['NAME_DB']),
        'USER': os.environ.get('DOC_USER', os.environ['USER_DB']),
        'PASSWORD': os.environ.get('DOC_PASSWORD', os.environ['PASSWORD_DB']),
        'HOST': os.environ.get('DOC_HOST_DB', os.environ['HOST_DB']),
        'PORT': os.environ.get('DOC_PORT_DB', os.environ['PORT_DB']),

        'DISABLE_SERVER_SIDE_CURSORS': True,

        'TEST': {'NAME': os.path.join(BASE_DIR, "test_db")}
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DATETIME_FORMAT = "d.m.Y G:i:s"

DATETIME_INPUT_FORMATS = ["d.m.Y G:i:s"]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = []

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'  # Перенаправление при успешном входе

AUTH_USER_MODEL = 'users.User'

#Project version
DEFAULT_VERSION = "2.1.0"

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Django auth backend
AUTHENTICATION_BACKENDS = (
    # social-oauth2
    # GitHub
    'social_core.backends.github.GithubOAuth2',

    # Google
    'social_core.backends.google.GoogleOAuth2',

    # Custom auth
    'src.users.auth.backends.CustomAuthBackend',

    # Django
    # 'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',

    # A custom "create_user" function add a 'slug' field to create a 'User' instance
    'src.users.auth.social_auth.create_user',

    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_PREFIX = "oauth"

# GitHub params
SOCIAL_AUTH_GITHUB_KEY = os.environ.get('DSA_GITHUB_KEY', os.environ['SA_GITHUB_KEY'])
SOCIAL_AUTH_GITHUB_SECRET = os.environ.get('DSA_GITHUB_SECRET', os.environ['SA_GITHUB_SECRET'])

# Google params
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('DSA_GOOGLE_OAUTH2_KEY', os.environ['SA_GOOGLE_OAUTH2_KEY'])
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('DSA_GOOGLE_OAUTH2_SECRET', os.environ['SA_GOOGLE_OAUTH2_SECRET'])


# JWTToken settings
JWT_SETTINGS = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=90),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=60),
    'ALGORITHM': 'HS256',

    'AUTH_HEADER_TYPES': 'Bearer',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('src.user.auth.models.JWTToken',), 
}


# Celery settings
REDIS_HOST = os.environ.get('DOC_HOST_CL', os.environ['REDIS_HOST'])
REDIS_PORT = 6379
REDIS_PASSWORD = os.environ.get('DOC_REDIS_PASSWORD', os.environ['REDIS_PASSWORD'])

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# CELERY_RESULT_EXPIRES = 3
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True


# smtp
EMAIL_HOST = os.environ.get('DOC_EMAIL_HOST', os.environ['EMAIL_HOST'])
EMAIL_PORT = 2525 #587
EMAIL_HOST_USER = os.environ.get('DOC_EMAIL_HOST_USER', os.environ['EMAIL_HOST_USER'])
EMAIL_HOST_PASSWORD = os.environ.get('DOC_EMAIL_HOST_PASSWORD', os.environ['EMAIL_HOST_PASSWORD'])
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False


# Other
INTERNAL_IPS = [
    'Redis',
    '0.0.0.0',
    '127.0.0.1',
]

# redis instance
redis_instance = redis.Redis(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    decode_responses=True,
    encoding="utf-8",
    )

# redis_instance.flushall()
