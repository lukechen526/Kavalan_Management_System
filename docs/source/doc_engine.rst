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
**Resource URL:** /api/documents , /api/documents/*document_id*/

**Supported methods:** GET

**Parameter:**

For /api/documents

- q(required): *JSON string of the search parameters (serial number/title, document level, and labels*)
- page_number(optional): *if there are more than one page of results (each page has 10 results), this specifies which page the server should return*

For /api/documents/*document_id*/

- None

**Response:** A JSON string containing the records matching the query, or an empty []

Example Request:

GET /api/documents?query={"sn_title":"he","document_level":"1","labels":["2"]}&page_number=1

(Shown as the original strings. In reality, they must be URL-encoded before sending.)

::

    {
    "page_number": 1,
    "num_pages": 1,
    "data":
        [
            {
                "title": "Test 124",
                "labels": [
                    {
                        "content": "TEST"
                    }
                ],
                "file_url": "/doc_engine/access/4/",
                "version": "1.0",
                "location": "",
                "serial_number": "HE 124"
            },
            
            {
                "title": "Home, sweet home",
                "labels": [
                    {
                        "content": "TEST"
                    }
                ],
                "file_url": "/doc_engine/access/10/",
                "version": "1.0",
                "location": "",
                "serial_number": "HE 123121212"
            }
        ]
    }
 
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

.. autofunction:: doc_engine.views.create_file_http_response

2. **Access recording:** Each time a user attempts to access a document, a record is written in the database, regardless of
the outcome (success or access denial).

.. autoclass:: doc_engine.models.AccessRecord

Batch Record
----------------

API
^^^^
**Resource URL:** /api/batchrecords , /api/batchrecords/*batchrecord_id*/
**Supported methods:** GET

**Parameters:**


All the parameters are enclosed in a JSON query string

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

GET /api/batchrecords?query={"name":"am","batch_number":"AMP12","date_manufactured_from":"2011-04-01","date_manufactured_to":"2011-09-06"}&page_number=1

(Shown as the original strings. In reality, they must be URL-encoded before sending.)

::

    {
        "page_number": 1,
        "num_pages": 1,
        "data": [
            {
                "date_manufactured": "2011-08-19",
                "batch_number": "AMP12",
                "name": "Ampicillin",
                "date_of_manufacture_in_minguo": "0100-08-19",
                "location": "AB 123"
            }
        ]
    }


Model
^^^^^^^

.. autoclass:: doc_engine.models.BatchRecord

Create/Update/Delete
^^^^^^^^^^^^^^^^^^^^^
Creating/updating/deleting of records is done via the Django admin interface.