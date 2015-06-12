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
    packages=['musette', 'musette.templatetags'],
    include_package_data=True,
    license='BSD License',
    zip_safe=False,
    description='Forum for Django framework.',
    long_description=README,
    url='https://github.com/mapeveri/django-musette',
    author='Peveri Martin',
    author_email='martinpeveri@gmail.com',
    install_requires=[
        'django-admin-log==0.2',
        'django-endless-pagination==2.1',
        'django-hitcount==1.0.5',
    ],
    dependency_links=[
        'https://github.com/mapeveri/django-endless-pagination/tarball/master#egg=django_endless_pagination-2.1',
        'https://github.com/mapeveri/django-hitcount/tarball/master#egg=django_hitcount-1.0.5',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
