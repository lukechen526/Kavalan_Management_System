# Django settings for Kavalan_Management_System project.
import os
import datetime

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DIRNAME = os.path.dirname(__file__)

ADMINS = (
    ('Yu-Po Luke Chen', 'nuemail@gmail.com'),
)

MANAGERS = ADMINS

INTERNAL_IPS = ('127.0.0.1',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'kavalan',                      # Or path to database file if using sqlite3.
        'USER': 'wufulab',                      # Not used with sqlite3.
        'PASSWORD': 'wufulab',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Taipei'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-tw'
ugettext = lambda s: s

LANGUAGES = (
  ('zh-tw', ugettext('Chinese-TW')),
  ('en', ugettext('English')),
)

NOTIFICATION_LANGUAGE_MODULE = 'accounts.UserProfile'

LOCALE_PATHS = (os.path.join(DIRNAME, 'locale'), )
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Use a directory inside the PROJECT_DIR for storing user-uploaded files during development
MEDIA_ROOT = os.path.join(DIRNAME, 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/uploads/'

#URL that points to the documentation
DOCUMENT_URL = '/docs/'

#The path to the built documentation
DOCUMENTATION_ROOT = os.path.join(DIRNAME, '../docs/build')

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(DIRNAME, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'secret'

LOGIN_URL ='/accounts/login/'
LOGIN_REDIRECT_URL = '/'
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'axes.middleware.FailedLoginMiddleware'
)

#Use DummyCache for development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

#User Console EmailBackbend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ROOT_URLCONF = 'kavalan.urls'


TEMPLATE_DIRS = (
        (os.path.join(DIRNAME, 'templates')),

)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'doc_engine',
    'accounts',
    'dynamo',
    'stream',
    'custom_notification',
    'axes',
    'notification',
    'south',
    'kavalan' #added to permit Javascript i18n
)

AUTH_PROFILE_MODULE = 'accounts.UserProfile'



#Configuration for Django-Axes
AXES_LOGIN_FAILURE_LIMIT = True
AXES_LOCK_OUT_AT_FAILURE = True
AXES_COOLOFF_TIME = datetime.timedelta(minutes=10)
AXES_LOCKOUT_TEMPLATE = 'registration/lockout.html'
AXES_LOCKOUT_URL = '/accounts/lockout/'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {

        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },

        'console':{
            'level':'ERROR',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console' ],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#Import settings_production.py for production environment
if not DEBUG:
    from settings_production import *
