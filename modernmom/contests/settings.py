from modernmom.settings_common import *

MEDIA_ROOT = '/home/www/modernmom.com/media/'
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
SITE_ID = 8

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'modernmom.urls.contests'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'connect.wsgi.application'

TEMPLATE_DIRS = (
    '/home/www/modernmom.com/templates/contests',
    '/home/www/modernmom.com/templates'
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

from modernmom.settings_INSTALLED_APPS import *



HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/modernmom'
    },
}

#Photologue
""" Got to be a better way to do this."""
import photologue, os, datetime
PHOTOLOGUE_DIR = 'uploads/contests'
def PHOTOLOGUE_PATH(instance, filename):
    f = datetime.datetime.now()
    datePath = '%d_%d_%d' % (f.year,f.month,f.day)
    p = os.path.join(PHOTOLOGUE_DIR, datePath) #, filename)
    if not os.path.exists(os.path.join(MEDIA_ROOT,p)):
        os.mkdir(os.path.join(MEDIA_ROOT,p))
    p = os.path.join(p, filename)
    return p


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
