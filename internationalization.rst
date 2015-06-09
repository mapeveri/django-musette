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

3. Add this snippet::

	{% load i18n %}

	<div id="lenguage_sel" class="pull-right">
				<form action="{% url 'set_language' %}" method="post" class="form-search">
					{% csrf_token %}
					<input name="next" type="hidden" value="{{ redirect_to }}" />
					<div class="input-group">
						<select class="form-control input-sm" name="language">
						{% get_current_language as LANGUAGE_CODE %}
						{% get_available_languages as LANGUAGES %}
						{% get_language_info_list for LANGUAGES as languages %}
						{% for language in languages %}
						<option value="{{ language.code }}"{% if language.code == LANGUAGE_CODE %} selected="selected"{% endif %}>
						    {{ language.name_local }} ({{ language.code }})
						</option>
						{% endfor %}
						</select>
						<span class="input-group-btn">
							<input type="submit" class="btn btn-flat btn-primary  btn-sm" value="Go" />
						</span>
					</div>
				</form>
			</div>

