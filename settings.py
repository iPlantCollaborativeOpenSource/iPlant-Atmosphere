#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Project: Atmosphere, iPlant Collaborative
# Author: Seung-jin Kim
# Twitter: @seungjin
# GitHub: seungjin
#

# Django settings for atmosphere project.


from ConfigParser import RawConfigParser

config = RawConfigParser()
config.read('/opt/atmo_home/credentials_never_git_it.ini')




#DATABASE_USER = config.get('database', 'DATABASE_USER')
#DATABASE_PASSWORD = config.get('database', 'DATABASE_PASSWORD')
#DATABASE_HOST = config.get('database', 'DATABASE_HOST')
#DATABASE_PORT = config.get('database', 'DATABASE_PORT')
#DATABASE_ENGINE = config.get('database', 'DATABASE_ENGINE')
#DATABASE_NAME = config.get('database', 'DATABASE_NAME')

DATABASES = {
    'default': {
        'ENGINE': 	'django.db.backends.'+config.get('database', 'DATABASE_ENGINE'), # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 	config.get('database', 'DATABASE_NAME'),                      # Or path to database file if using sqlite3.
        'USER': 	config.get('database', 'DATABASE_USER'),                      # Not used with sqlite3.
        'PASSWORD': 	config.get('database', 'DATABASE_PASSWORD'),                  # Not used with sqlite3.
        'HOST': 	config.get('database', 'DATABASE_HOST'),                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': 	config.get('database', 'DATABASE_PORT'),                      # Set to empty string for default. Not used with sqlite3.
	'OPTIONS':	{
	}
    }
}


#TEST_DATABASE_NAME = config.get('database', 'TESTSUITE_DATABASE_NAME')

#SECRET_KEY = config.get('secrets','SECRET_KEY')
#CSRF_MIDDLEWARE_SECRET = config.get('secrets', 'CSRF_MIDDLEWARE_SECRET')

#SESSION_COOKIE_DOMAIN = config.get('cookies','SESSION_COOKIE_DOMAIN')

#DEBUG = config.getboolean('debug','DEBUG')
#TEMPLATE_DEBUG = config.getboolean('debug','TEMPLATE_DEBUG')
#VIEW_TEST = config.getboolean('debug', 'VIEW_TEST')
#INTERNAL_IPS = tuple(config.get('debug', 'INTERNAL_IPS').split())
#if config.getboolean('debug', 'SKIP_CSRF_MIDDLEWARE'):
#    MIDDLEWARE_CLASSES = tuple([x for x in list(MIDDLEWARE_CLASSES)
#                                  if not x.endswith('CsrfMiddleware')])

SERVER_EMAIL = config.get('email', 'SERVER_EMAIL')
EMAIL_HOST = config.get('email', 'EMAIL_HOST')
ADMINS = tuple(config.items('error mail'))
MANAGERS = tuple(config.items('404 mail'))


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    (config.get('admins', 'name'), config.get('admins', 'email')),
)

MANAGERS = ADMINS


#DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#DATABASE_NAME = ''             # Or path to database file if using sqlite3.
#DATABASE_USER = ''             # Not used with sqlite3.
#DATABASE_PASSWORD = ''         # Not used with sqlite3.
#DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
#DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Phoenix'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
#SECRET_KEY = 'asdasd123489dskfjh8293kjdhn8923yuidsfhiudsf8923iufhiwdufh2389j'
SECRET_KEY = config.get('secrets','SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
  #'django.template.loaders.filesystem.load_template_source',
  'django.template.loaders.filesystem.Loader',
  'django.template.loaders.app_directories.load_template_source',
  #django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'atmosphere.urls'

import os.path
import djcelery

djcelery.setup_loader()
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"


BROKER_HOST = config.get('celery', 'BROKER_HOST') 
BROKER_PORT = config.get('celery', 'BROKER_PORT')
BROKER_USER = config.get('celery', 'BROKER_USER')
BROKER_PASSWORD = config.get('celery', 'BROKER_PASSWORD')
BROKER_VHOST = config.get('celery', 'BROKER_VHOST')

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

	os.path.join(os.path.dirname(__file__),'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'atmosphere.cloudservice',
    'atmosphere.cloudauth',
    'atmosphere.cloudfront',
    'djcelery',
    'atmosphere.cloudservice.scheduler',
    'django.contrib.admin', #activate admin 
)

# The age of session cookies, in seconds.
# http://docs.djangoproject.com/en/dev/ref/settings/
# http://docs.djangoproject.com/en/dev/topics/http/sessions/#topics-http-sessions
# Now I set sessio cookies life time = 3600 seconds = 1 hour
#SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

## LDAP BACKEND
## http://packages.python.org/django-auth-ldap/
#import ldap
#from django_auth_ldap.config import LDAPSearch, GroupOfNamesType


# Baseline configuration.
#AUTH_LDAP_SERVER_URI = "ldap://ldap.iplantcollaborative.org"

#AUTH_LDAP_BIND_DN = "cn=django-agent,dc=example,dc=o"
#AUTH_LDAP_BIND_PASSWORD = "phlebotinum"
#AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=users,dc=example,dc=com",
#    ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
# or perhaps:
#AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,ou=people,dc=iplantcollaborative,dc=org"

# Set up the basic group parameters.
#AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=people,dc=iplantcollaborative,dc=org",
#    ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)"
#)
#AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="ou")

# Only users in this group can log in.
#AUTH_LDAP_REQUIRE_GROUP = "ou=people,dc=iplantcollaborative,dc=org"

# Populate the Django user from the LDAP directory.
#AUTH_LDAP_USER_ATTR_MAP = {
#    "first_name": "givenName",
#    "last_name": "sn",
#    "email": "mail"
#}

#AUTH_LDAP_PROFILE_ATTR_MAP = {
#    "employee_number": "employeeNumber"
#}
#
#AUTH_LDAP_USER_FLAGS_BY_GROUP = {
#    "is_active": "cn=active,ou=django,ou=groups,dc=example,dc=com",
#    "is_staff": "cn=staff,ou=django,ou=groups,dc=example,dc=com",
#    "is_superuser": "cn=superuser,ou=django,ou=groups,dc=example,dc=com"
#}

# This is the default, but I like to be explicit.
#AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Use LDAP group membership to calculate group permissions.
#AUTH_LDAP_FIND_GROUP_PERMS = True

# Cache group memberships for an hour to minimize LDAP traffic
#AUTH_LDAP_CACHE_GROUPS = True
#AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600


# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    #'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
## END OF LDAP BACKEND


## logging
import logging
logging.basicConfig (
	level = logging.DEBUG,
	format = '%(asctime)s %(levelname)s %(message)s',
	filename = os.path.dirname(__file__)+'/./logs/atmosphere.log',
	filemode = 'a'
)
## end of logging

DEFAULT_CHARSET = "utf-8"

import sys
sys.stdout = sys.stderr
