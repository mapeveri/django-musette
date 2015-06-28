import os

from django.conf import settings
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP


settings.configure(
	DEBUG = False,
	ALLOWED_HOSTS = ['*'],
	SECRET_KEY='Musette Rock!',
	INSTALLED_APPS = (
	    'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.messages',
	    'django.contrib.staticfiles',
	    'log',
	    'hitcount',
	    'endless_pagination',
	    'musette',
	    'musette_tests',
	),
	MIDDLEWARE_CLASSES = (
	    'django.contrib.sessions.middleware.SessionMiddleware',
	    'django.middleware.common.CommonMiddleware',
	    'django.middleware.csrf.CsrfViewMiddleware',
	    'django.contrib.auth.middleware.AuthenticationMiddleware',
	    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	    'django.contrib.messages.middleware.MessageMiddleware',
	    'django.middleware.clickjacking.XFrameOptionsMiddleware',
	    'django.middleware.security.SecurityMiddleware',
	    'django.middleware.locale.LocaleMiddleware',
	),
	TEMPLATE_CONTEXT_PROCESSORS = TCP + (
	    "django.core.context_processors.i18n",
	    "django.core.context_processors.request",
	),
	LOGIN_URL = "/",
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.sqlite3',
	        'NAME': 'db.sqlite3',
	    }
	},
	CACHES = {
	    'default': {
	        'BACKEND' : 'redis_cache.RedisCache',
	        'LOCATION' : 'localhost:6379',
	        'OPTIONS' : {
	            'DB' : 1
	            #'PASSWORD' :'asdas6d87sf6tsd8f',
	            }
	        }
	},
	LANGUAGE_CODE = 'en',
	TIME_ZONE = 'America/New_York',
	USE_I18N = True,
	USE_L10N = True,
	USE_TZ = True,
	SESSION_SAVE_EVERY_REQUEST = True,
	APP_PROFILE = 'main',
	MODEL_PROFILE = 'Perfil',
	FIELD_PHOTO_PROFILE = "photo",
	URL_PROFILE = '/profile/',
)