from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = True

ALLOWED_HOSTS = [
    'podiam.app',
    'www.podiam.app',
    '35.183.155.122',
    'frontend-pulpit.vercel.app',
    'localhost',
    '127.0.0.1',
]

# Security settings for SSL/HTTPS with nginx
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False
USE_X_FORWARDED_HOST = True  # Add this for nginx proxy compatibility


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    "corsheaders",
    "django_rest_passwordreset",
    'users',
    'candidates',
    'example',
    'rest_framework.authtoken',
    'storages',
    'allauth',
    'allauth.account',
    'allauth.headless',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    "django_celery_results"
]


AWS_ACCESS_KEY_ID = "AKIAUPMYMZSPX7ZEN3WI"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "pulpit"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"


SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600000
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    'allauth.account.auth_backends.AuthenticationBackend',
]

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'
CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False

# Use specific domains instead of wildcard
CSRF_TRUSTED_ORIGINS = [
    'https://podiam.app',
    'https://www.podiam.app',
    'http://podiam.app',
    'http://www.podiam.app',
    'https://35.183.155.122',
    'http://localhost:3000',
    'https://frontend-pulpit.vercel.app'
]

ROOT_URLCONF = 'api.urls'

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
AUTH_USER_MODEL= 'users.User'
WSGI_APPLICATION = 'api.wsgi.app'


#EMAIL_HOST = os.environ["EMAIL_HOST"]
#EMAIL_PORT = int(os.environ["EMAIL_PORT"])
EMAIL_USE_TLS = True
#EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
#EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_DEBUG = True

INTERNAL_IPS = [
    "127.0.0.1",
    "35.183.155.122"
]

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# Note: Django modules for using databases are not support in serverless
# environments like Vercel. You can use a database over HTTP, hosted elsewhere.

if os.getenv("DB_NAME") and not DEBUG:  # use postgres if env variables are configured
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ["DB_NAME"],
            "USER": os.environ["DB_USER"],
            "PASSWORD": os.environ["DB_PASSWORD"],
            "HOST": os.environ["DB_HOST"],
            "PORT": os.environ["DB_PORT"],  # 5432 by default
        }
    }

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ["DB_NAME"],
            "USER": os.environ["DB_USER"],
            "PASSWORD": os.environ["DB_PASSWORD"],
            "HOST": os.environ["DB_HOST"],
            "PORT": os.environ["DB_PORT"],  # 5432 by default
        }
    }

"""
 DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
"""

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

MEDIA_ROOT= os.path.join(BASE_DIR,'media')
MEDIA_URL='/media/'


REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.TokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        ),
        'DEFAULT_PARSER_CLASSES': [
            'rest_framework.parsers.JSONParser',
            'rest_framework.parsers.FormParser',
            'rest_framework.parsers.MultiPartParser',
        ],
        'DEFAULT_RENDERER_CLASSES': [
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ],
    }

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_EXPOSE_HEADERS = ['content-type', 'x-csrftoken']

CORS_ALLOWED_ORIGINS = [
    'https://podiam.app',
    'https://www.podiam.app',
    'http://podiam.app',
    'http://www.podiam.app',
    'https://35.183.155.122',
    'http://localhost:3000',
    'https://frontend-pulpit.vercel.app'
]

# For some environments, this may be necessary
CORS_ORIGIN_WHITELIST = CORS_ALLOWED_ORIGINS

# For browsers that don't support CORS preflight requests
CORS_ALLOW_ALL_ORIGINS = True  # Changed based on reference project

# Keep it true for authentication to work properly
CORS_ALLOW_CREDENTIALS = True

# Set CSRF allowed origins same as CORS
CSRF_ALLOWED_ORIGINS = CORS_ALLOWED_ORIGINS

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SITE_ID = 1

HEADLESS_ONLY = True
HEADLESS_FRONTEND_URLS = {
    "account_confirm_email": "/account/verify-email/{key}",
    "account_reset_password": "/account/password/reset",
    "account_reset_password_from_key": "/account/password/reset/key/{key}",
    "account_signup": "/account/signup",
    "socialaccount_login_error": "/account/provider/callback",
}


# ---------------------------------------------REDIS SETTINGS------------------------------------------------------
#REDIS_HOST = "127.0.0.1"
#REDIS_PORT = 6379
#REDIS_DB = 0


#CELERY_BROKER_URL = f"redis://:{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
CELERY_BROKER_URL = "redis://localhost:6379/0"

CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Kolkata" #change timezone based on server time
USE_TZ = True
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"