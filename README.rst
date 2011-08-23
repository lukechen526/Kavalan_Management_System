Introduction
===============
Kavalan Management System is a Enterprise Resource Planning (ERP_) application suite designed to facilitate the business processes at small- to medium-size firms.
It is currently being developed with the support of `Wu-Fu Laboratories, Ltd`_. The system aims to be `PIC/S`_ compliant.

Sub-systems
================
Several apps have been planned for inclusion in the suite. They are all at very early stage of development

- *Doc Engine* for document search and retrieval
- *Dynamo* for creating database query dynamically based on user input.
- Stream (for posting status updates and sharing links)
- Inventory Management
- Account and Profile Management
- The *API* sub-system is used to centralize the management of public APIs exposed by the other sub-systems.


Author(s)
===========
Luke (Yu-Po) Chen, nuemail@gmail.com

Dependencies
==================

- Python >= 2.6
- Django 1.3
- `Django-piston`_ >= 0.2.2
- `pyPDF`_ >= 1.13 and `ReportLab ToolKit`_ >= 2.5
- `guess-language`_ >=0.2
- `South`_ >= 0.7.3
- `Django-axes`_ >= 0.1.1
_ `Django-notification`_ >= 0.2.0
- Sphinx >= 1.0.7
- Database connectors for MySQL or PostgreSQL

.. _ERP: http://en.wikipedia.org/wiki/Enterprise_resource_planning
.. _Wu-Fu Laboratories, Ltd: http://www.wufulab.com
.. _Django-piston: https://bitbucket.org/jespern/django-piston/wiki/Home
.. _PIC/S: http://www.picscheme.org/
.. _pyPDF: http://pybrary.net/pyPdf/
.. _ReportLab ToolKit: http://www.reportlab.com/software/opensource/rl-toolkit/
.. _South: http://south.aeracode.org/
.. _Django-axes: http://code.google.com/p/django-axes/
.. _guess-language: http://pypi.python.org/pypi/guess-language
.. _Django-notification: https://github.com/jtauber/django-notification

