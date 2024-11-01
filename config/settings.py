import os
from datetime import timedelta
from pathlib import Path
from typing import List

from corsheaders.defaults import default_headers

from pydantic_settings import BaseSettings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%6md%hcvsly=tz7-3ej_9t6yu)%i6uqb#c=r!1lpm543k%#j43'


class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str

    REDIS_HOST: str = ''
    REDIS_PORT: str = ''
    REDIS_PASSWORD: str = ''
    DEBUG: bool = True

    ALLOWED_HOSTS: List[str] = ['*']

    CORS_ALLOW_ALL_ORIGINS: bool = True

    CSRF_TRUSTED_ORIGINS: List[str] = ['http://*', 'https://*']

    class Config:
        env_file = BASE_DIR / '.env'


settings = Settings()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = settings.DEBUG

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # applications
    'apps.quizzes.apps.QuizzesConfig',
    'apps.questions.apps.QuestionsConfig',
    'apps.question_options.apps.QuestionOptionsConfig',
    'apps.utils.apps.UtilsConfig',
    'apps.groups.apps.GroupsConfig',
    'apps.users.apps.UsersConfig',

    # dependencies
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'corsheaders',
    'django_filters'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_PAGINATION_CLASS': 'config.paginator.StandardResultsSetPagination',
    'PAGE_SIZE': 20
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': settings.DB_NAME,
        'USER': settings.DB_USER,
        'PASSWORD': settings.DB_PASS,
        'HOST': settings.DB_HOST,
        'PORT': settings.DB_PORT,
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
}

# Password validation
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

# Swagger settings
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'},
    },
    'DEEP_LINKING': True,
}

AUTH_USER_MODEL = 'users.User'

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# Media files (Images, Videos, Files)
MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_HEADERS = [
    *default_headers,
    "password-for-receipts",
]

CORS_ALLOW_ALL_ORIGINS = settings.CORS_ALLOW_ALL_ORIGINS

CSRF_TRUSTED_ORIGINS = settings.CSRF_TRUSTED_ORIGINS

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://:{redis_password}@{redis_host}:{redis_port}".format(
            redis_host=settings.REDIS_HOST,
            redis_port=settings.REDIS_PORT,
            redis_password=settings.REDIS_PASSWORD
        ),
        'TIMEOUT': None,
    }
}
