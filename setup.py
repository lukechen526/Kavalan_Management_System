#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

import kavalan
version = kavalan.__version__

setup(
    name = "django-kavalan",
    version = version,
    url = 'https://github.com/lukechen526/Kavalan_Management_System',
    download_url = 'https://github.com/lukechen526/Kavalan_Management_System/zipball/master',
    license = 'BSD',
    description = "Kavalan Management System, a Enterprise Resource Planning (ERP) application suite designed to facilitate the business processes at small- to medium-size firms.",
    author = 'Yu-Po Luke Chen',
    author_email = 'nuemail@gmail.com',
    packages = find_packages(),
    namespace_packages = ['kavalan'],
    include_package_data = True,
    zip_safe = False,
    classifiers = [
        'Development Status :: 4 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
  