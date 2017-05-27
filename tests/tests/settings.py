import os

from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings.configure(
    DEBUG=False,
    ALLOWED_HOSTS=['*'],
    SECRET_KEY='Musette Rock!',
    INSTALLED_APPS=(
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'hitcount',
        'endless_pagination',
        'musette',
        'musette_tests',
    ),
    MIDDLEWARE_CLASSES=(
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
    LOGIN_URL="/",
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    LANGUAGE_CODE='en',
    TIME_ZONE='America/New_York',
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
    SITE_NAME='Musette Forum',
    SITE_URL='http://localhost:800/',
    EMAIL_MUSETTE='',
    STATIC_ROOT=os.path.join(BASE_DIR, 'staticfiles'),
    STATIC_URL='/static/',
    STATICFILES_DIRS=(
        os.path.join(BASE_DIR, 'static'),
    ),
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
)
