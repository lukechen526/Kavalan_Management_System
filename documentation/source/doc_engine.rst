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
API
^^^^^^^^
**GET /documents/**

**Resource URL:** /api/documents/

**Parameter:** q(required)= *title or document serial number to query against*

**Response:** A JSON string containing the records matching the query, or an empty []

Example Request:

GET /api/documents/?q=AF




Model
^^^^^^^
::

    class Document(models.Model):
        """
        Model for digitally stored documents
        """
        serial_number = models.CharField(max_length=50, unique='True', verbose_name=ugettext_lazy('Document Serial Number'))
        title = models.CharField(max_length=100, verbose_name=ugettext_lazy('Title'))
        author = models.CharField(max_length=100, default='Wufulab Ltd', verbose_name=ugettext_lazy('Author'))
        version = models.IntegerField(verbose_name=ugettext_lazy('Version'))
        file = models.FileField(upload_to='documents', verbose_name=ugettext_lazy('File'))
        last_updated = models.DateTimeField(verbose_name=ugettext_lazy('Last Updated'), auto_now=True)
        permitted_groups = models.ManyToManyField(Group, blank=True, verbose_name=ugettext_lazy('Permitted Groups'))

        class Meta:
            verbose_name = ugettext_lazy('Document')
            verbose_name_plural = ugettext_lazy('Document')

        def file_url(self):
            return "/doc_engine/access/%s/" % self.pk

        def __unicode__(self):
            return unicode(self.serial_number)


Create/Update/Delete
^^^^^^^^^^^^^^^^^^^^^
Creating/updating/deleting of records is done via the Django admin interface.


Access Control
^^^^^^^^^^^^^^^^
Access control is performed via the view DocumentAccess. Every document can be accessed at /doc_engine/access/*pk*/ .

.. autofunction:: doc_engine.views.DocumentAccess


Batch Record
----------------

API
^^^^
**GET /batchrecords/**

**Resource URL:** /api/batchrecords/

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

GET /api/batchrecords/?name=Ampi&batch_number=&date_manufactured_from=2011-07-07&date_manufactured_to=
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
::

    class BatchRecord(models.Model):
        """
        Model for batch records
        """
        name = models.CharField(max_length=30, verbose_name=ugettext_lazy('Product Name'))
        batch_number = models.CharField(max_length=30, verbose_name=ugettext_lazy('Batch Number'))
        serial_number = models.IntegerField(verbose_name=ugettext_lazy('Serial Number'))
        date_manufactured = models.DateField(verbose_name=ugettext_lazy('Date Manufactured'))
        location = models.CharField(max_length=30, verbose_name=ugettext_lazy('Physical Location'))

        class Meta:
            verbose_name = ugettext_lazy('Batch Record')
            verbose_name = ugettext_lazy('Batch Record')

        def __unicode__(self):
            return unicode(self.batch_number)

        def save(self, *args, **kwargs):
            if self.date_manufactured.year <= 1000:
                #Convert MINGUO Year to CE before saving
                self.date_manufactured = self.date_manufactured.replace(year=self.date_manufactured.year+MINGUO)
            super(BatchRecord, self).save(*args, **kwargs)


Create/Update/Delete
^^^^^^^^^^^^^^^^^^^^^
Creating/updating/deleting of records is done via the Django admin interface.