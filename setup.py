#!/usr/bin/env python
import os
import sys
from setuptools import setup

sys.path.insert(0, 'musette')
from version import get_version
sys.path.remove('musette')

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='django-musette',
    version=get_version(),
    packages=[
        'musette', 'musette.templatetags',
        'musette.websockets', 'musette.management',
        'musette.management.commands',
    ],
    include_package_data=True,
    license='BSD License',
    zip_safe=False,
    description='Forum for Django framework.',
    long_description=README,
    url='https://github.com/mapeveri/django-musette',
    author='Peveri Martin',
    author_email='martinpeveri@gmail.com',
    install_requires=[
        'tornado==4.2',
        'django-redis-cache==1.6.5',
        'djangorestframework==3.3.3',
        'django-endless-pagination-angular==1.1',
        'django-hitcount==1.2.1'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
