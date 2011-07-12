.. _intro:

Project Overview
===================

Introduction
--------------------

Kavalan Management System is an enterprise resource planning (ERP_) application suite designed to facilitate the business processes at small- to medium-size firms.
It is currently being developed with the support of `Wu-Fu Laboratories, Ltd`_

Sub-systems
--------------------
Several apps have been planned for inclusion in the suite. They are all at very early stage of development:

- *Doc Engine* for document search and retrieval
- *Dynamo* for creating database query dynamically based on user input.
- Inventory Management
- Account and Profile Management
- The *API* sub-system is used to centralize the management of public APIs exposed by the other sub-systems.

Dependencies
--------------------

- Python >= 2.6
- Django 1.3
- `Django-Piston`_ >= 0.2.2
- Python database connectors for MySQL or PostgreSQL

.. _ERP: http://en.wikipedia.org/wiki/Enterprise_resource_planning
.. _Wu-Fu Laboratories, Ltd: http://www.wufulab.com
.. _Django-piston: https://bitbucket.org/jespern/django-piston/wiki/Home
