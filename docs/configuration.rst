Installing
----------

With pip::

	pip install django-musette


Quick start
-----------

1. Add application 'musette' and dependencies to INSTALLED_APPS::

	INSTALLED_APPS = (
		'django.contrib.admin',
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.messages',
		'django.contrib.staticfiles',
		'django.contrib.sites',
		...
		'hitcount',
		'endless_pagination',
		'rest_framework',
		'musette',
		...
		# Your local apps
	)

2. Add this urls to file urls.py::

	url(r'^' , include('musette.urls')),

	....

	# And add this at the end of the file
	from django.conf import settings
	
	if settings.DEBUG:
	    from django.conf.urls.static import static
	    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

3. In settings.py configure LOGIN_URL, STATIC_ROOT, STATICFILES_DIRS, STATIC_URL, MEDIA_URL, MEDIA_ROOT, SITE_ID, SITE_NAME and SITE_URL. `Example config`_ of settings.py.

.. _Example config: https://github.com/mapeveri/django-musette/blob/master/example/tests/settings.py	

4. In settings.py in TEMPLATES check in context_processors this values::

		'django.template.context_processors.debug',
		'django.template.context_processors.request',
		'django.contrib.auth.context_processors.auth',
		'django.contrib.messages.context_processors.messages',
		'django.template.context_processors.media',
		'django.template.context_processors.static',
		'django.template.context_processors.tz',
		'django.template.context_processors.i18n',
		'musette.context_processors.data_templates', # Necessary

5. Configure in the settings.py the variable CACHES for redis. This is for real time support. Example::

		CACHES = {
			'default': {
			    'BACKEND' : 'redis_cache.RedisCache',
			    'LOCATION' : 'localhost:6379',
			    'OPTIONS' : {
			        'DB' : 1
			        }
			    }
		}

6. In MIDDLEWARE_CLASSES add this line::

        MIDDLEWARE_CLASSES = (
                ...
				'musette.middleware.ActiveUserMiddleware', # Necessary
				'musette.middleware.RestrictStaffToAdminMiddleware' # If you want block admin url add this middleware
        )

7. Execute command migrate::

	python manage.py migrate

	# If your super-admin user not contain the record in Profile model. Execute this command:
	python manage.py create_profile_superadmin # New in version 0.2.5

9. Configuration internationalization in English or `forum in spanish or italian`_.

.. _forum in spanish or italian: https://github.com/mapeveri/django-musette/blob/master/docs/internationalization.rst

10. Config variables to send email and variable EMAIL_MUSETTE with email from in settings.py.

11. Set variable GOOGLE_MAPS_API_KEY with API_KEY value of `Google maps`_. (New in version 0.2.8)

NOTE: Before adding the superuser, make sure that the steps are executed correctly, so django-musette can create the super-user user profile automatically.

NOTE2: For `custom user model`_.

.. _custom user model: https://github.com/mapeveri/django-musette/blob/master/docs/custom-user-model.rst

.. _Google maps: https://developers.google.com/maps/faq?hl=es-419#new-key
