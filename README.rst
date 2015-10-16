==============
Django-Musette
==============


.. image:: https://coveralls.io/repos/mapeveri/django-musette/badge.svg
  :target: https://coveralls.io/r/mapeveri/django-musette

.. image:: https://travis-ci.org/mapeveri/django-musette.svg?branch=master
    :target: https://travis-ci.org/mapeveri/django-musette

.. image:: https://badge.fury.io/py/django-musette.svg
    :target: http://badge.fury.io/py/django-musette

.. image:: https://img.shields.io/pypi/dm/django-musette.svg
   :target: https://pypi.python.org/pypi/django-musette

Forum for Django framework. This reusable application it is designed to be easily integrated into an existing Django application.

Installing
----------

With pip::

	pip install django-musette

Requirements
------------

1. Jquery (Version 2.x)
2. Bootstrap (Version 3.x) and `bootstrap material design`_.
3. Angular.js (Version 1.x)

.. _bootstrap material design: https://fezvrasta.github.io/bootstrap-material-design/

Quick start
-----------

1. Add application 'musette' and dependencies to INSTALLED_APPS::

	INSTALLED_APPS = (
		...
		'log',
		'hitcount',
		'endless_pagination',
		'rest_framework',
		'musette',
	)

2. Add this urls to file urls.py::

	url(r'^' , include('musette.urls')),

3. And in settings.py add this variable::

	SESSION_SAVE_EVERY_REQUEST = True

4. Configure in the settings.py URL_LOGIN, STATIC and MEDIA root. Something very important is to set the variable CACHES for redis. example::

	CACHES = {
	    'default': {
	        'BACKEND' : 'redis_cache.RedisCache',
	        'LOCATION' : 'localhost:6379',
	        'OPTIONS' : {
	            'DB' : 1
	            }
	        }
	}

5. Set this variables if differ from the default values::

	APP_PROFILE = 'profiles' # Application for your profiles
	MODEL_PROFILE = 'Profile' # Model for profiles
	FIELD_PHOTO_PROFILE = "photo" # Field that contains url the profile photo
	URL_PROFILE = '/profile/' # Url for profile
	URL_PROFILE_PARAMS = ("username",) # Params of url profile, indicate field user model

6. Execute command migrate::

	python manage.py migrate

7. The application django-musette need a template base of name base.html. With the following tags::

	{% block content %}{% endblock %}
	{% block extra_css %}{% endblock %}
	{% block extra_js %}{% endblock %}
	{% block hitcount_javascript %}{% endblock %}

	//And add files static css and js (Angular, Jquery, Bootstrap).

8. `Example base`_ of base.html.

.. _Example base: https://github.com/mapeveri/django-musette/blob/master/example/plantillas/base.html

9. If you need to enable the `forum in spanish`_.

.. _forum in spanish: https://github.com/mapeveri/django-musette/blob/master/internationalization.rst

How to use?
-----------

1. Login in django admin and start to insert categories necessary. Example:

.. image:: https://github.com/mapeveri/django-musette/blob/master/images/categories.png

The field position is for indicate the order of the categories.

2. Insert the forum necessary: Example:

.. image:: https://github.com/mapeveri/django-musette/blob/master/images/forums.png

Field more importants:

	- Position: The field position is for indicate the order of the forums in the categories.
	- Topics count: Total forum topics.
	- Check topics: If you need to review the topics by a moderator.

3. **Make sure that each user registration exist in the profile table.**

Ready!

Execute in the terminal::

	python manage.py runserver

4. In other terminal execute this command for run server tornado for web sockets::

	python manage.py musette_run_server_ws

Visit 127.0.0.1:8000/forums you should see the categories and forums.

.. image:: https://github.com/mapeveri/django-musette/blob/master/images/index.png

.. image:: https://github.com/mapeveri/django-musette/blob/master/images/forum.png

.. image:: https://github.com/mapeveri/django-musette/blob/master/images/notifications.png

.. image:: https://github.com/mapeveri/django-musette/blob/master/images/topic.png

.. image:: https://github.com/mapeveri/django-musette/blob/master/images/new_comment.png

.. image:: https://github.com/mapeveri/django-musette/blob/master/images/comment.png

.. image:: https://github.com/mapeveri/django-musette/blob/master/images/new_topic.png

.. image:: https://github.com/mapeveri/django-musette/blob/master/images/edit_topic.png

Features
--------

1. Multiple forums ordered by for category.
2. Notifications (Still not support sending emails).
3. Notifications and comments in real time.
4. Count views for forum and topic.
5. Infinite scroll for comments of one topic.
6. Support of files media for topics.
7. Easy integration with other applications Django of your project.
8. Pre-moderation of topics.
9. Models registered in admin django for administrators.
10. Search for topics in a forum.
11. Modern design, thank you to Bootstrap material design.
12. Avatar.
13. Support to English and Spanish language.
14. Validation of forms in real time with AngularJs.
15. User registration a forum.
16. Support to Markdown.
17. Support to rss to forums.
18. API REST with django-rest-framework.
19. Support to topics main in forum.

Roadmap
-------

`Roadmap`_ with content of the next versions of django-musette.

.. _Roadmap: https://github.com/mapeveri/django-musette/blob/master/roadmap.rst

Contribute
----------

1. Fork this repo and install it
2. Follow PEP8, Style Guide for Python Code
3. Write code
4. Write unit test
5. Send pull request
