"""
Django settings for LabMAN project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

"""Installed PyPI packages:
Django (1.8.4)
django-autocomplete-light (2.2.5)
django-colorful (1.1.0)
django-filebrowser (3.5.7)
django-gfklookupwidget (1.0.3)
django-grappelli (2.7.1)
django-rulez (1.0.2)
django-sitetree (1.4.0)
django-tinymce (2.0.4)
django-phonenumber-field 1.0.0
bleach
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from ConfigParser import RawConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = RawConfigParser()
config.read(os.path.join(BASE_DIR,'settings.ini'))

DATABASE_USER = config.get('database', 'DATABASE_USER')
DATABASE_PASSWORD = config.get('database', 'DATABASE_PASSWORD')
DATABASE_HOST = config.get('database', 'DATABASE_HOST')
DATABASE_ENGINE = config.get('database', 'DATABASE_ENGINE')
DATABASE_NAME = config.get('database', 'DATABASE_NAME')

SECRET_KEY = config.get('security','SECRET_KEY')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'grappelli', #django-grapelli package
    'filebrowser', # django-filebrowser package
    'tinymce', # django-tinymce package
    'sitetree', # django-sitetree package
    'rulez', # django-rulez package
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'colorful', # django-colorful package
    'tagged_object', #provide support for things with category/tags
    'mime_typed_object',#Provide support for objects with mime_types
    'equipment',
    'img',
    'files',
    'pages',
    'user_profile',
)

LABMAN_APPS={
        "equipment":["Equipment"],
        "user_profile":["Person"],
        "pages":["Page"]
    }

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
)

ROOT_URLCONF = 'LabMAN.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                "django.core.context_processors.request",
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LabMAN.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': DATABASE_ENGINE,
        'NAME': DATABASE_NAME,
        'HOST': DATABASE_HOST,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'GMT'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,"static")

MEDIA_ROOT = os.path.join(BASE_DIR,"media")
MEDIA_URL = "/media/"

# Flatpages

SITE_ID = 1

# Filebrowser for TinyMCE

FILEBROWSER_VERSIONS_BASEDIR = '_versions'
FILEBROWSER_DIRECTORY = ''

#TinyMCE editor for text areas

TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace,lists,code,anchor,wordcount",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True

# Auth settings

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', # Django's default auth backend
    'rulez.backends.ObjectPermissionBackend',
]
