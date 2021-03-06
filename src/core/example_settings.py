#!/usr/bin/env python -W ignore::DeprecationWarning
__copyright__ = "Copyright 2017 Birkbeck, University of London"
__author__ = "Martin Paul Eve & Andy Byers"
__license__ = "AGPL v3"
__maintainer__ = "Birkbeck Centre for Technology and Publishing"

"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import logging

from django.contrib import messages

from core import plugin_installed_apps

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "plugins"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# You should change this key before you go live!
SECRET_KEY = 'uxprsdhk^gzd-r=_287byolxn)$k6tsd8_cepl^s^tms2w1qrv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',

    # Installed Apps
    'cms',
    'core',
    'copyediting',
    'cron',
    'events',
    'identifiers',
    'journal',
    'metrics',
    'preprint',
    'press',
    'production',
    'proofing',
    'review',
    'security',
    'submission',
    'transform',
    'utils',

    # 3rd Party
    'django_summernote',
    'dynamicsites',
    'markdown_deux',
    'foundationform',
    'hvad',
    'raven.contrib.django.raven_compat',
    'bootstrap4',
]

INSTALLED_APPS += plugin_installed_apps.load_plugin_apps()
INSTALLED_APPS += plugin_installed_apps.load_homepage_element_apps()

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'core.middleware.SiteSettingsMiddleware',
    'utils.template_override_middleware.ThemeEngineMiddleware',
    'core.middleware.MaintenanceModeMiddleware',
    'cron.middleware.CronMiddleware',
    'core.middleware.CounterCookieMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'templates', 'admin')] + plugin_installed_apps.load_plugin_templates() +
        plugin_installed_apps.load_homepage_element_templates(),
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.journal',
                'core.context_processors.journal_settings',
                'core.context_processors.press',
                'core.context_processors.active',
                'core.context_processors.navigation',
                'django_settings_export.settings_export',
                'django.template.context_processors.i18n'
            ],
            'loaders': [
                'utils.template_override_middleware.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

SETTINGS_EXPORT = [
    'ORCID_API_URL',
    'ORCID_TOKEN_URL',
    'ORCID_CLIENT_SECRET',
    'ORCID_CLIENT_ID',
    'ORCID_URL'
]


WSGI_APPLICATION = 'core.wsgi.application'
SITES_DIR = os.path.join(os.path.dirname(__file__), 'sites')
DEFAULT_HOST = 'www.example.org'  # This is the default redirect if no other sites are found.

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
# We recommend mysql but Django supports PGSQL and SQLite amongst others

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'core', 'locales')
]


def ugettext(s):
    return s


LANGUAGES = (
    ('en', ugettext('English')),
    ('fr', ugettext('French')),
    ('de', ugettext('German')),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

USE_I18N = True
USE_L10N = False
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'collected-static')
STATICFILES_DIRS = (
    # The /src/static/ folder is used by Janeway and should not be removed.
    os.path.join(BASE_DIR, 'static'),
)
STATIC_URL = '/static/'


SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode
    'iframe': False,  # or set False to use SummernoteInplaceWidget - no iframe mode

    # Using Summernote Air-mode
    'airMode': True,

    # Use native HTML tags (`<b>`, `<i>`, ...) instead of style attributes
    # (Firefox, Chrome only)
    'styleWithTags': True,

    # Set text direction : 'left to right' is default.
    'direction': 'ltr',

    # Change editor size
    'width': '100%',
    'height': '480',

    # Need authentication while uploading attachments.
    'attachment_require_authentication': True,
}

# 1.9 appears confused about where null and blank are required for many to
# many fields, so we're hiding these warning from the console
SILENCED_SYSTEM_CHECKS = (
    'fields.W340',
)

'''
# This section should only be enabled if you intend to use Sentry for error reporting.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR', # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
RAVEN_CONFIG = {
    'dsn': '',
}
'''


class SuppressDeprecated(logging.Filter):
    def filter(self, record):
        WARNINGS_TO_SUPPRESS = [
            'RemovedInDjango110Warning',
        ]
        # Return false to suppress message.
        return not any([warn in record.getMessage() for warn in WARNINGS_TO_SUPPRESS])


MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

LOGIN_REDIRECT_URL = '/user/profile/'
LOGIN_URL = '/login/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''
EMAIL_PORT = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True


DATE_FORMT = "Y-m-d"
DATETIME_FORMAT = "Y-m-d H:i"

AUTH_USER_MODEL = 'core.Account'

PLUGIN_HOOKS = {}

NOTIFY_FUNCS = []

ORCID_API_URL = 'https://pub.orcid.org/v1.2_rc7/'
ORCID_URL = 'https://orcid.org/oauth/authorize'
ORCID_TOKEN_URL = 'https://pub.orcid.org/oauth/token'
ORCID_CLIENT_SECRET = ''
ORCID_CLIENT_ID = ''


SESSION_COOKIE_NAME = 'JANEWAYSESSID'

S3_ACCESS_KEY = ''
S3_SECRET_KEY = ''
S3_BUCKET_NAME = ''
END_POINT = 'eu-west-2'  # eg. eu-west-1
S3_HOST = 's3.eu-west-2.amazonaws.com'  # eg. s3.eu-west-1.amazonaws.com

BACKUP_TYPE = 'directory'  # s3 or directory
BACKUP_DIR = '/path/to/backup/dir/'
BACKUP_EMAIL = False # If set to True, will send an email each time backup is run
