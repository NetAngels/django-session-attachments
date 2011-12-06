#!/usr/bin/env python
# -*- coding: utf8 -*-
from distutils.core import setup
import os
import sys

reload(sys).setdefaultencoding("UTF-8")


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except:
        return ''

setup(
    name='django-session-attachments',
    version='0.1',
    author='NetAngels',
    author_email='info@netangels.ru',
    packages=['session_attachments'],
    url='http://github.com/NetAngels/django-session-attachments',
    license='BSD License',
    description=(u'Django app to handle attachments (temporary uploads) '
                 u'grouped by sessions and bundles. Even for anonymous users'),
    long_description=read('README.rst'),
    install_requires=['Django', ],
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
)
