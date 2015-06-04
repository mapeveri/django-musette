#!/usr/bin/env python
import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='django-musette',
    version='0.4',
    packages=['musette', 'musette.templatetags'],
    include_package_data=True,
    license='MIT',
    zip_safe=False,
    description='Forum for django framework.',
    long_description=README,
    url='https://github.com/mapeveri/django-musette',
    author='Peveri Martin',
    author_email='martinpeveri@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django-admin-log==0.2',
    ],
)

os.system('pip install -e git://github.com/thornomad/django-hitcount.git@602038c445a55db4b9d33a9c1b6929c09539d42f#egg=django_hitcount-master')
os.system('pip install -e git://github.com/webstack/django-endless-pagination.git@0ed7376fa461345d96ce62541816dd3550bb0d25#egg=django_endless_pagination')
