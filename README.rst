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

Features
--------

1. Multiple forums ordered by for category.
2. Support to sub-forums.
3. Count views for forum and topic.
4. Support to topics main in forum.
5. Support to rss to forums.
6. User registration a forum.
7. Search topics in a forum.
8. Pre-moderation of topics with multiple moderators.
9. Support of media files for topics.
10. Infinite scroll for comments of one topic.
11. Notifications and email notifications.
12. Notifications and comments in real time.
13. Integrated model profile, but can be extended.
14. Avatar profile.
15. Easy integration with other applications Django of your project.
16. Models registered in admin django for administrators.
17. Support check user online.
18. Support to English and Spanish languages.
19. Validation of forms in real time with AngularJs.
20. API REST with django-rest-framework.
21. Support Python 3.
22. Custom configuration css.
23. Markdown support in textarea.
24. Authentication.
25. Message for forums.
26. Suggested Topics in topic.
27. Close topic.

**Note 1:** When a new record is added to the user model automatically added to your model profile.

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
	)

2. Add this urls to file urls.py::

	url(r'^' , include('musette.urls')),

	....

	# And add this
	from django.conf import settings
	
	if settings.DEBUG:
	    from django.conf.urls.static import static
	    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

3. In settings.py configure LOGIN_URL, STATIC, MEDIA root, SITE_ID, SITE_NAME and SITE_URL. `Example config`_ of settings.py.

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
		'musette.middleware.ActiveUserMiddleware', # Necessary
		'musette.middleware.RestrictStaffToAdminMiddleware' # If you want block admin url add this middleware

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
                'musette.middleware.ActiveUserMiddleware',
        )

7. In your application must add the profile model do the following. For example your app is 'main', in models.py and admin.py add::
	
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

8. Execute command migrate::

	python manage.py makemigrations 
	python manage.py migrate

	python manage.py makemigrations musette
	python manage.py migrate musette

9. If you need to enable the `forum in spanish`_.

.. _forum in spanish: https://github.com/mapeveri/django-musette/blob/master/internationalization.rst

10. Config variables to send email and variable EMAIL_MUSETTE with email from in settings.py.
	

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

3. Add record to Model Configuration and configurate the forum.

4. **Make sure that each user registration exist in the profile table.** Execute in the terminal::

	python manage.py runserver

5. In other terminal execute this command for run server tornado for web sockets::

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
