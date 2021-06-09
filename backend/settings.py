"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

import os
import requests
import environ


def env_var(VAR_NAME):
    try:
        if VAR_NAME not in os.environ:
            env = environ.Env()
            env.read_env()
            os.environ[VAR_NAME] = env(VAR_NAME)
        return os.environ[VAR_NAME]
    except:
        error_msg = 'Set the {} environment variable'.format(var_name)
        raise Exception(error_msg)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env_var('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_var('DEBUG')

# Fix enhanced health overview false negative:
# Get IP address of the EC2 instance that sends the health check request to
# Django so we can add it to ALLOWED_HOSTS and change the 4xx error it
# returns into a 3xx error.Django returns the 3xx error when an http request
# is sent, since it requires all requests be sent with https.


def get_ec2_instance_ip():
    try:
        ip = requests.get(
            'http://169.254.169.254/latest/meta-data/local-ipv4',
            timeout=0.01
        ).text
    except requests.exceptions.ConnectionError:
        return None
    return ip


AWS_LOCAL_IP = get_ec2_instance_ip()

ALLOWED_HOSTS = [
    'localhost',
    'freshi-prod.us-east-1.elasticbeanstalk.com',
    'freshi-staging.us-east-1.elasticbeanstalk.com',
    AWS_LOCAL_IP
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_admin_inline_paginator',
    'rest_framework',
    'corsheaders',
    'environ',
    'django_apps',
    'django_apps.website',
    'django_apps.foods',
    'django_apps.users',
    'django_apps.recipes',
    'django_apps.media',
    'django_apps.api_auth',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

# The order of AUTHENTICATION_BACKENDS matters, so if the same
# username and password is valid in multiple backends, Django
# will stop processing at the first positive match.
# If a backend raises a PermissionDenied exception, authentication
# will immediately fail. Django won’t check the backends that follow.
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

REST_FRAMEWORK = {
    # Determines the default set of authenticators used when accessing the
    # request.user or request.auth properties. All authenticators must
    # pass for all drf views.
    # This is why we cannot add APIAuthentication
    # here, or else all views including the one to get the Authorization
    # token would be protected by the Authorization token.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    # Determines the default set of permissions checked at the start of a view.
    # Permission must be granted by every class in the list.
    'DEFAULT_PERMISSION_CLASSES': [
        # Anyone can access API endpoints by default
        'rest_framework.permissions.AllowAny',
    ]
}

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Add the root folder of frontend to serve front and back end
        # at port 8000.
        'DIRS': [os.path.join(BASE_DIR, 'frontend')],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env_var('DB_NAME'),
        'USER': env_var('DB_USER'),
        'PASSWORD': env_var('DB_PASSWORD'),
        'HOST': env_var('DB_HOST'),
        'PORT': env_var('DB_PORT'),
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.' +
        'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.' +
        'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.' +
        'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.' +
        'NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.User'


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT is where static files are placed after collectstatic.
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATICFILES_DIRS is where collectstatic can find static files that it will
# collect.
STATICFILES_DIRS = (
    # Add the build directory from the frontend directory to serve front and
    # back end at port 8000.
    os.path.join(BASE_DIR, 'frontend', "build", "static"),
)

# S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = env_var('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = env_var('AWS_S3_REGION_NAME')
AWS_ACCESS_KEY_ID = env_var('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env_var('AWS_SECRET_ACCESS_KEY')

FRESHI_AUTH_ACCESS_KEY = env_var('FRESHI_AUTH_ACCESS_KEY')
