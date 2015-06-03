1. In the settings.py add::

	from django.utils.translation import ugettext_lazy as _
	from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP


	MIDDLEWARE_CLASSES = (
	    ...
	    'django.middleware.locale.LocaleMiddleware',
	)

	TEMPLATE_CONTEXT_PROCESSORS = TCP + (
	    "django.core.context_processors.i18n",
	    "django.core.context_processors.request",
	)

	LANGUAGE_CODE = 'es'

	# Lenguage support
	LANGUAGES = (
	    ('en', _('English')),
	    ('es', _('Spanish')),
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
