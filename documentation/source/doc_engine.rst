.. _doc-engine:

Doc Engine
===========

Overview
---------

Doc Engine is the system for document search and retrieval. It deals with the following data types:

- **Document**: a digital document file residing on the server.
- **BatchRecord**: a searchable record in the database that points to the physical location of a batch record

Model
------------
::

    class Document(models.Model):
        serial_number = models.CharField(max_length=50, unique='True', verbose_name=ugettext_lazy('Document Serial Number'))
        title = models.CharField(max_length=100, verbose_name=ugettext_lazy('Title'))
        author = models.CharField(max_length=100, default='Wufulab Ltd', verbose_name=ugettext_lazy('Author'))
        version = models.IntegerField(verbose_name=ugettext_lazy('Version'))
        file = models.FileField(upload_to='documents', verbose_name=ugettext_lazy('File'))
        last_updated = models.DateTimeField(verbose_name=ugettext_lazy('Last Updated'), auto_now=True)


*Document* is exposed via /api/documents 