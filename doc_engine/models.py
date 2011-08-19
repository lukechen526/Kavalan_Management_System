from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver


class DocumentLabel(models.Model):
    content = models.CharField(max_length=30, verbose_name=ugettext_lazy('Label'))

    class Meta:
        verbose_name = ugettext_lazy('Label')
        verbose_name_plural = ugettext_lazy('Labels')

    def __unicode__(self):
        return self.content

class Document(models.Model):
    """
    Model for digitally stored documents. The model doesn't actually store the file path; it only stores the version
    number, then delegates the task of storing the file to FileObject, which has a ForeignKey to the Document model.
    
    - serial_number: CharField
    - title: CharField
    - author: CharField
    - version: CharField
    - last_updated: DateTimeField
    - permitted_groups: ManytoManyField

    """

    serial_number = models.CharField(max_length=50, unique='True', verbose_name=ugettext_lazy('Document Serial Number'))
    title = models.CharField(max_length=100, verbose_name=ugettext_lazy('Title'))
    labels = models.ManyToManyField(DocumentLabel, verbose_name=ugettext_lazy('Labels'), blank=True)
    author = models.CharField(max_length=100, default='Wufulab Ltd', verbose_name=ugettext_lazy('Author'))
    version = models.CharField(max_length=10, default='1.0', verbose_name=ugettext_lazy('Active Version'))
    last_updated = models.DateTimeField(verbose_name=ugettext_lazy('Last Updated'), auto_now=True)
    permitted_groups = models.ManyToManyField(Group, blank=True, verbose_name=ugettext_lazy('Permitted Groups'))
    DOCUMENT_LEVELS = (
        ('1', ugettext_lazy('Level 1')),
        ('2', ugettext_lazy('Level 2')),
        ('3', ugettext_lazy('Level 3')),
        ('4', ugettext_lazy('Level 4')),
        )
    document_level = models.CharField(max_length=1, default='4',choices=DOCUMENT_LEVELS, verbose_name=ugettext_lazy('Document Level'))
    searchable = models.BooleanField(default=False, verbose_name=ugettext_lazy('Searchable'))
    
    class Meta:
        verbose_name = ugettext_lazy('Document')
        verbose_name_plural = ugettext_lazy('Documents')
        
    def file_url(self):
        return "/doc_engine/access/%s/" % self.pk

    def file(self):
        #Get the file that corresponds to the current version
        return self.versions.get(version__exact=self.version).file

    def __unicode__(self):
        return unicode(u'%s %s' %(self.serial_number, self.title))


class FileObject(models.Model):
    """
    Model for storing the file path to the actual file on the disk and the version number. It then points
    to the Document object.

    - document: ForeignKey to Document
    - file: FileField
    - version: CharField
    - uploaded_date: DateTimeField, auto_now_add=True
    
    """
    document = models.ForeignKey(Document, related_name='versions')
    file = models.FileField(upload_to='documents', verbose_name=ugettext_lazy('File'))
    version = models.CharField(max_length=10, verbose_name=ugettext_lazy('Version'))
    uploaded_date = models.DateTimeField(auto_now=True)
    revision_comment = models.TextField(default='', verbose_name=ugettext_lazy('Revision Comment'), blank=True)

    class Meta:
        verbose_name = ugettext_lazy('File Object')
        verbose_name_plural = ugettext_lazy('File Objects')
        
    def __unicode__(self):
        return unicode(u'%s %s' %(self.document, self.version))

@receiver(pre_delete, sender=FileObject)
def on_delete_FileObject(sender, **kwargs):
    """
    When a FileObject row is being removed from the database, deletes the associated file from storage. In addition,
    changes the version of the Document it is associated with to the latest one, or makes the Document unsearchable
    if there is no other version.
    """
    file_obj = kwargs['instance']
    file_obj.file.delete()
    
    try:
        file_obj.document.version = file_obj.document.versions.exclude(id=file_obj.id).latest('uploaded_date').version
    except FileObject.DoesNotExist:
        file_obj.document.searchable = False
        
    file_obj.document.save()

class AccessRecord(models.Model):
    """
    Model for recording the access of any document by any user

    - user: ForeignKey
    - access_time: DateTimeField
    - ip: IPAddressField
    - document_accessed: ForeignKey
    - success: BooleanField

    """
    user = models.ForeignKey(User, verbose_name=ugettext_lazy('User') )
    access_time = models.DateTimeField(auto_now_add=True, verbose_name=ugettext_lazy('Access Time'))
    ip = models.IPAddressField(verbose_name=ugettext_lazy('IP'))
    document_accessed = models.ForeignKey(Document, verbose_name=ugettext_lazy('Document Accessed'))
    success = models.BooleanField(verbose_name=ugettext_lazy('Success?'))

    class Meta:
        verbose_name = ugettext_lazy('Access Record')
        verbose_name_plural = ugettext_lazy('Access Records')
        permissions = (
            ("view_accessrecord", "Can view but not add/change/delete records"),
        )
        ordering = ['-access_time', 'user']

    def __unicode__(self):
        if self.success:
            return u"%s: %s %s %s" %(ugettext_lazy('SUCCESS'),self.user, self.document_accessed, self.access_time.isoformat(' '))
        else:
            return u"%s: %s %s %s" %(ugettext_lazy('FAILURE'),self.user, self.document_accessed, self.access_time.isoformat(' '))

class BatchRecord(models.Model):
    """
    Model for batch records

    - name: CharField
    - batch_number: CharField
    - serial_number: IntegerField
    - date_manufactured: DateField
    - location: CharField

    """
    name = models.CharField(max_length=30, verbose_name=ugettext_lazy('Product Name'))
    batch_number = models.CharField(max_length=30, verbose_name=ugettext_lazy('Batch Number'))
    serial_number = models.IntegerField(verbose_name=ugettext_lazy('Serial Number'))
    date_manufactured = models.DateField(verbose_name=ugettext_lazy('Date Manufactured'))
    location = models.CharField(max_length=30, verbose_name=ugettext_lazy('Physical Location'))

    class Meta:
        verbose_name = ugettext_lazy('Batch Record')
        verbose_name_plural = ugettext_lazy('Batch Records')
        
    def __unicode__(self):
        return unicode(self.batch_number)

    def date_manufactured_minguo(self):
        return self.date_manufactured.replace(year=self.date_manufactured.year-1911)


    

