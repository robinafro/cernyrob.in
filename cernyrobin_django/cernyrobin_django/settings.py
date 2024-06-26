"""
Django settings for cernyrobin_django project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import dotenv, os

try:
    dotenv.load_dotenv()
except Exception as e:
    print("Failed to load dotenv file. This should only happen in a docker container!")
    print(e)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("LOCAL") == "1"


ALLOWED_HOSTS = ["*", ".localhost", ".autokafka.cz", "localhost", "autokafka.cz", "me", "10.1.2.6", "192.168.219.42", ".autokafka.cz", "autokafka.cz", "api.autokafka.cz" "www.autokafka"]

CSRF_TRUSTED_ORIGINS = [
    "https://autokafka.cz",
    "https://www.autokafka.cz",
    "https://api.autokafka.cz",
    "http://autokafka.cz",
    "http://www.autokafka.cz",
    "http://api.autokafka.cz",


    "http://localhost",    
    "https://.autokafka.cz",
    "https://autokafka.cz",
    "http://autokafka.cz",
    "https://.localhost",
    "http://.autokafka.cz",
    "http://.localhost",
    "http://127.0.0.1",
    "http://me",
    "http://10.1.2.6",
    "http://192.168.219.42",
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "corsheaders",
    'cernyrobin_app',
    'api',
    "kafka",
    "ads",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cernyrobin_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'cernyrobin_django.wsgi.application'

# CORS
# CORS_ALLOWED_ORIGINS = [
#     "https://autokafka.cz",
#     "http://localhost",    
#     "https://.autokafka.cz",
#     "https://.localhost",
#     "http://.autokafka.cz",
#     "http://.localhost"
# ]

CORS_ALLOW_ALL_ORIGINS = True

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Delete the SESSION_COOKIE_DOMAIN code below if logging in seems to be broken
SESSION_COOKIE_DOMAIN = ".autokafka.cz"

if os.getenv("LOCAL") == "1":
    SESSION_COOKIE_DOMAIN = None

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static/'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media/'

STATICFILES_DIRS = []

if DEBUG:
    STATIC_ROOT = None
    STATICFILES_DIRS = [STATIC_URL]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
