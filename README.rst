==============
Django-Musette
==============

Forum for Django framework.

NOTE: This application is under development. It is not recommended to use in a production environment.

Installing
----------

pip install django-musette

Requirements:
-------------

1. Jquery
2. Bootstrap and bootstrap material desing (https://fezvrasta.github.io/bootstrap-material-design/)

Quick start:
------------

1. Add application 'musette' and dependencies to INSTALLED_APPS::

	INSTALLED_APPS = (
			...
			'log',
    		'hitcount',
    		'endless_pagination',
    		'musette',
	)

2. Add this urls to file urls.py::

	from hitcount.views import update_hit_count_ajax

	url(r'^ajax/hit/$', update_hit_count_ajax,
        name='hitcount_update_ajax'),
	url(r'^' , include('musette.urls')),

3. And in settings.py add this variable::

	SESSION_SAVE_EVERY_REQUEST = True

4. Configure STATIC and MEDIA root in the settings.py::

5. Set this variables::

	APP_PROFILE = 'profiles' # Application for your profiles
	MODEL_PROFILE = 'Profile' # Model for profiles
	FIELD_PHOTO_PROFILE = "photo" # Field that contains url photo
	URL_PROFILE = '/profile/' # Url for profile

6. Execute command migrate::

	python manage.py migrate

7. The application django-musette need a template base of name base.html. Example:

	https://github.com/mapeveri/django-musette/blob/master/tests/plantillas/base.html

	With the following tags::
		{% block content %}{% endblock %}
		{% block hitcount_javascript %}{% endblock %}
		{% block extra_js %}{% endblock %}

8. If you need Spanish forum enable internationalization in django.

	https://github.com/mapeveri/django-musette/blob/master/internationalization.rst

How to use?:
------------

1. Login in django admin and start to insert categories necessary. Example:

.. image:: https://github.com/mapeveri/django-musette/blob/master/images/categories.png

The field position is for indicate the order of the categories.

2. Insert the forum necessary: Example:

.. image:: https://github.com/mapeveri/django-musette/blob/master/images/forums.png

Field more importants:

	- Position: The field position is for indicate the order of the forums in the categories.
	- Topics count: Total forum topics.
	- Check topics: If you need to review the topics by a moderator.

Ready!


Execute in the terminal::

	python manage.py runserver

Visit 127.0.0.1:8000/forums you should see the categories and forums.

.. image:: https://github.com/mapeveri/django-musette/blob/master/images/index.png