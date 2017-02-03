1. In the settings.py add::

	from django.utils.translation import ugettext_lazy as _

	MIDDLEWARE_CLASSES = (
	    ...
	    'django.middleware.locale.LocaleMiddleware',
	)

	TEMPLATES = [
	    {
	        'BACKEND': 'django.template.backends.django.DjangoTemplates',
	        'DIRS': [os.path.join(BASE_DIR, "plantillas")],
	        'APP_DIRS': True,
	        'OPTIONS': {
	            'context_processors': [
	            	....
	                'django.template.context_processors.i18n',
	            ],
	        },
	    },
	]

	LANGUAGE_CODE = 'es'

	# Lenguage support
	LANGUAGES = (
	    ('en', _('English')),
	    ('es', _('Spanish')), # For Spanish
		('it', _('Italian')), # For Italian
	)

	# Path of the folder locale
	LOCALE_PATHS = (
	    os.path.join(BASE_DIR, 'locale'),
	)

	TIME_ZONE = 'America/Buenos_Aires'
	USE_I18N = True
	USE_L10N = True
	USE_TZ = True


2. In the urls.py add this url::

	url(r'^i18n/', include('django.conf.urls.i18n')),
