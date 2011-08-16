.. _doc-engine:

Doc Engine
===========

Overview
---------

Doc Engine is the system for document search and retrieval. It current handles the following data types

- **Document**: a database record for a digital file residing on the server.
- **BatchRecord**: a searchable record in the database that points to the physical location of a batch record

Doc Engine applies strict access control and records all requests for documents in the database. 

Client-Server Communication
------------------------------
The search functionality of *Doc Engine* is exposed via its public API

``/api/documents`` for Document search
``/api/batchrecords`` for Batch Record search

Document
-------------------------
Search API
^^^^^^^^^^^^^
**GET /documents**

**Resource URL:** /api/documents

**Parameter:** q(required)= *title or document serial number to query against*

**Response:** A JSON string containing the records matching the query, or an empty []

Example Request:

GET /api/documents?q=Lab
::

    [
        {
            "serial_number": "Lab 101",
            "version": 1.3,
            "file_url": "/doc_engine/access/1/",
            "title": "Lab 101 SOP"
        }
    ]
 
Model
^^^^^^^

There are two models for storing documents in Doc Engine: Document and FileObject. **Document** stores the metadata about each document, i.e.
the serial number, title, and group permission. It also contains a version number that corresponds to a **FileObject**, which stores the file path
to the actual file on the disk.
The user can change the version number for a given Document instance and have it serve a specific version of the file.


.. autoclass:: doc_engine.models.Document
.. autoclass:: doc_engine.models.FileObject

Create/Update/Delete
^^^^^^^^^^^^^^^^^^^^^
Creating/updating/deleting of records is done via the Django admin interface

.. _doc-engine-security:

Access the actual file and security
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The search result provides a link to the actual file at /doc_engine/access/*primary key*/ . Access control is employed to
ensure that only authorized users are permitted to access the document.

Security is ensured through the following mechanisms:

1. **Group-based permission model:** Each Document has a set of permitted groups. When a user tries to access the document,
his/her group membership is checked against that of the Document. Only a user who passes the test will be given access to the file.
Others will see "Access Denied."

.. autofunction:: doc_engine.views.createFileHttpResponse

2. **Access recording:** Each time a user attempts to access a document, a record is written in the database, regardless of
the outcome (success or access denial).

.. autoclass:: doc_engine.models.AccessRecord

3. **Watermarking of PDF documents:** If the document to be accessed is a PDF file, an access watermark is added to the bottom of every page,
specifying the user who downloaded the file and the time of access.

.. autofunction:: doc_engine.views.createPDFHttpResponse

Batch Record
----------------

API
^^^^
**GET /batchrecords**

**Resource URL:** /api/batchrecords

**Parameters:**

+---------------------------------------+-----------------------------------------------+
|                                       |                                               |
+=======================================+===============================================+
| **name** *optional*                   |Product name for the batch record              |
+---------------------------------------+-----------------------------------------------+
| **batch_number** *optional*           |Batch number of the batch record               |
+---------------------------------------+-----------------------------------------------+
| **date_manufactured_from** *optional* |Specify the date range to search for           |
|                                       |                                               |
| **date_manufactured_to** *optional*   |[date_manufactred_from, date_manufactured_to]  |
+---------------------------------------+-----------------------------------------------+

**At least one parameter has to be non-empty, otherwise the server returns a 400 error.**

**Response:** A JSON string containing the records matching the query, or an empty []

Example Request:

GET /api/batchrecords?name=Ampi&batch_number=&date_manufactured_from=2011-07-07&date_manufactured_to=
::

    [
        {
            "date_manufactured": "2011-07-08",
            "batch_number": "AM12",
            "name": "Ampicillin",
            "location": "A-12"
        }
    ]


Model
^^^^^^^

.. autoclass:: doc_engine.models.BatchRecord

Create/Update/Delete
^^^^^^^^^^^^^^^^^^^^^
Creating/updating/deleting of records is done via the Django admin interface.