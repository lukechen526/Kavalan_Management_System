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
- Stream (for posting status updates and sharing links)
- Forum (based on a modified version of LBForum)
- Account and Profile Management
- The *API* sub-system is used to centralize the management of public APIs exposed by the other sub-systems.

Dependencies
--------------------

- Python >= 2.6
- Django 1.3
- `Django-piston`_ >= 0.2.2
- `pyPDF`_ >= 1.13 and `ReportLab ToolKit`_ >= 2.5
- `guess-language`_ >=0.2
- `South`_ >= 0.7.3
- `Django-axes`_ >= 1.2.4
- `Django-notification`_ >= 0.2.0
- `LBForum`_ >= 0.9.20
- Sphinx >= 1.0.7
- Database connectors for MySQL or PostgreSQL

Author(s)
---------------

Luke (Yu-Po) Chen, nuemail@gmail.com

LICENSE
----------------
::

    Copyright 2011, Wu-Fu Laboratories Co, Ltd. and individual contributors. All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are
    permitted provided that the following conditions are met:

       1. Redistributions of source code must retain the above copyright notice, this list of
          conditions and the following disclaimer.

       2. Redistributions in binary form must reproduce the above copyright notice, this list
          of conditions and the following disclaimer in the documentation and/or other materials
          provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY WU-FU LABORATORIES CO, LTD. ``AS IS'' AND ANY EXPRESS OR IMPLIED
    WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
    FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL WU-FU LABORATORIES CO, LTD. OR
    CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
    ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
    ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    The views and conclusions contained in the software and documentation are those of the
    authors and should not be interpreted as representing official policies, either expressed
    or implied, of  Wu-Fu Laboratories Co,Ltd.


.. _ERP: http://en.wikipedia.org/wiki/Enterprise_resource_planning
.. _Wu-Fu Laboratories, Ltd: http://www.wufulab.com
.. _Django-piston: https://bitbucket.org/jespern/django-piston/wiki/Home
.. _PIC/S: http://www.picscheme.org/
.. _pyPDF: http://pybrary.net/pyPdf/
.. _ReportLab ToolKit: http://www.reportlab.com/software/opensource/rl-toolkit/
.. _South: http://south.aeracode.org/
.. _Django-axes: http://pypi.python.org/pypi/django-axes/
.. _guess-language: http://pypi.python.org/pypi/guess-language
.. _LBForum: https://github.com/lukechen526/LBForum
.. _Django-notification: https://github.com/jtauber/django-notification