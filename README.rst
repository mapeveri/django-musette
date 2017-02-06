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
18. Support to English, Italian and Spanish languages.
19. Validation of forms in real time with VueJs.
20. API REST with django-rest-framework.
21. Support Python 3.
22. Custom configuration css.
23. Markdown support in textarea.
24. Authentication.
25. Message for forums.
26. Suggested Topics in topic.
27. Close topic.
28. Support to custom user model.
29. Support to likes in topics and comments.
30. Check if a user is a troll.

**Note 1:** When a new record is added to the user model automatically added to your model profile.


Configuration and installation
------------------------------

`Documentation`_ for installation and configuration

.. _Documentation: https://github.com/mapeveri/django-musette/blob/master/docs/configuration.rst


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

3. Add record to Model Configuration and configurate the forum (Css styles, logo forum, etc).

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
