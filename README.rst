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

3. And in settings.py in TEMPLATES check in context_processors this values::

	'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'django.template.context_processors.i18n',
    'musette.context_processors.data_templates',

4. Configure in the settings.py LOGIN_URL, STATIC and MEDIA root. Something very important is to set the variable CACHES for redis. This is for real time support. Example::

	CACHES = {
	    'default': {
	        'BACKEND' : 'redis_cache.RedisCache',
	        'LOCATION' : 'localhost:6379',
	        'OPTIONS' : {
	            'DB' : 1
	            }
	        }
	}

5. In your application add the profile model do the following. For example your app is 'main', In models.py and admin.py add::
	
	# models.py
	from musette.models import AbstractProfile

	class Profile(AbstractProfile):

		# This is in case you need to extend the profile model. If not use 'pass'
		location = models.CharField("Label name", max_length=200, null=True, blank=True)
		company = models.CharField("Label name", max_length=150, null=True, blank=True)

	# admin.py
	from .models import Profile

	admin.site.register(Profile)

	# If you need to extend so, you will create template profile.html indide your app and add this
	# templates/main/profile.html

	<h4>Location</h4>
	<div class="panel panel-default">
	    <div class="panel-body">
	        {{ profile.location|safe }}
	    </div>
	</div>

	<h4>Company</h4>
	<div class="panel panel-default">
	    <div class="panel-body">
	        {{ profile.company|safe }}
	    </div>
	</div>

6. Execute command migrate::

	python manage.py migrate
	python manage.py makemigrations
	python manage.py migrate


7. If you need to enable the `forum in spanish`_.

.. _forum in spanish: https://github.com/mapeveri/django-musette/blob/master/internationalization.rst

8. Config variables to send email and variable EMAIL_MUSETTE with email from in settings.py.

9. In settings.py configure SITE_NAME and SITE_URL. `Example config`_ of settings.py.		
		
.. _Example config: https://github.com/mapeveri/django-musette/blob/master/example/tests/settings.py

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

3. **Make sure that each user registration exist in the profile table.** Execute in the terminal::

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
2. Notifications and email notifications.
3. Notifications and comments in real time.
4. Count views for forum and topic.
5. Infinite scroll for comments of one topic.
6. Support of media files for topics.
7. Easy integration with other applications Django of your project.
8. Pre-moderation of topics.
9. Models registered in admin django for administrators.
10. Search for topics in a forum.
11. Modern design, thank you to Bootstrap material design.
12. Avatar.
13. Support to English and Spanish languages.
14. Validation of forms in real time with AngularJs.
15. User registration a forum.
16. Support to Markdown.
17. Support to rss to forums.
18. API REST with django-rest-framework.
19. Support to topics main in forum.
20. Integrated model profile, but can be extended.

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
