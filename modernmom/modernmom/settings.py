# Django settings for modernmom project.
SESSION_COOKIE_DOMAIN = '.modernmom.com'
CSRF_COOKIE_DOMAIN = '.modernmom.com'
SECRET_KEY = 'jkie34!c06a2f0#ao5wr)tx!in@%_dour=ywc=1_=0g&b=hx!o'
LOGIN_REDIRECT_URL = '/'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
          ('Justin', 'justin@modernmom.com'),
)

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'members@modernmom.com'
EMAIL_HOST_PASSWORD = 'MMemail2@'


MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'modernmom_django_production',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'modernmom',
        'PASSWORD': 'm0d3rnm0m!',
        'HOST': 'f9ac11c65dc06de81a21930d127dee38081ca5d8.rackspaceclouddb.com',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

AUTH_USER_MODEL = 'members.Member'

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages",
"django.core.context_processors.request",
 'modernmom.context_processors.taxonomy',
 'modernmom.context_processors.featured',
 'modernmom.context_processors.site_processor',
 'jumplinks.context_processors.jumplinks',)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['www.modernmom.com',]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
SITE_URL = 'http://modernmom.com'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True
MEDIA_ROOT = '/home/www/modernmom.com/media/'
MEDIA_URL = '/media/'
STATIC_ROOT = '/home/www/modernmom.com/static/'
STATIC_URL = '/static/'

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
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'modernmom.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'modernmom.wsgi.application'

TEMPLATE_DIRS = (
                 '/home/www/modernmom.com/templates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.redirects',
    'photologue','tagging',
    'members','django_twitter',
    'taxonomy','articles','featured_content',
    'contests','django.contrib.flatpages','toolbox',
    'django_bootstrap_wysiwyg',
    #'redactor',
    'newsletter','cissonius','jumplinks'
    #'south',
     #'survey','voting','cissonius',
     #'toolbox','scoop','contests','featured_content',
    
     
   # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)
LOGIN_URL = '/login/'
WYSIWYH_DEFAULT_TOOLBAR_ITEMS = [
    'font_size', 
    'font_weights', 
    'lists',
    'alignments', 
    'hyperlink', 
    'image','video',
    'speech',
    'source'  # only available for chrome
]

#Photologue
""" Got to be a better way to do this."""
import photologue, os, datetime
PHOTOLOGUE_DIR = 'uploads/'
def PHOTOLOGUE_PATH(instance, filename):
    f = datetime.datetime.now()
    datePath = '%d_%d_%d' % (f.year,f.month,f.day)
    p = os.path.join(PHOTOLOGUE_DIR, datePath) #, filename)
    if not os.path.exists(os.path.join(MEDIA_ROOT,p)):
        os.mkdir(os.path.join(MEDIA_ROOT,p))
    p = os.path.join(p, filename)
    return p

#REDACTOR_OPTIONS = {'lang': 'en'}
#REDACTOR_UPLOAD = 'uploads/'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/modernmom'
    },
}
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
