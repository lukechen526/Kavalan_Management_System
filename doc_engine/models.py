from django.db import models
from django import forms
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver

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
    author = models.CharField(max_length=100, default='Wufulab Ltd', verbose_name=ugettext_lazy('Author'))
    version = models.CharField(max_length=10, default='1.0', verbose_name=ugettext_lazy('Active Version'))
    last_updated = models.DateTimeField(verbose_name=ugettext_lazy('Last Updated'), auto_now=True)
    permitted_groups = models.ManyToManyField(Group, blank=True, verbose_name=ugettext_lazy('Permitted Groups'))

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
    uploaded_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ugettext_lazy('File Object')
        verbose_name_plural = ugettext_lazy('File Objects')
        
    def __unicode__(self):
        return unicode(u'%s %s' %(self.document, self.version))

@receiver(pre_delete, sender=FileObject)
def deleteFileOnServer(sender, **kwargs):
    """
    When a FileObject row is being removed from the database, deletes the associated file from storage.
    """
    file_obj = kwargs['instance']
    file_obj.file.delete()

@receiver(post_delete, sender=FileObject)
def deleteDocumentWithZeroVersion(sender, **kwargs):
    """
    After a FileObject is deleted, if the Document it points to no longer has any associated FileObjects,
    this function removes it from the database.
    """
    file_obj = kwargs['instance']
    try:
        if file_obj.document.versions.count() == 0 :
            file_obj.document.delete()
    except Document.DoesNotExist:
        pass

class DocumentForm(forms.ModelForm):
    file = forms.FileField(label=ugettext_lazy('File'), required=False,
                           help_text=ugettext_lazy("Upload a new version of the document, or keep the same version number but\
                           upload a new file to overwrite the old one. \
                           If you are just changing the version number, do not upload any file." ))

    version = forms.CharField(label=ugettext_lazy('Active Version'),
                              initial='1.0',
                              help_text=ugettext_lazy('Enter a new version number, or pick a previous version number to make it active.'))
    class Meta:
        model = Document

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


class BatchRecordInputForm(forms.ModelForm):
    date_manufactured = forms.DateField(label=ugettext_lazy('Date of Manufacture'))
    class Meta:
        model = BatchRecord

class BatchRecordSearchForm(forms.Form):
    name = forms.CharField(label=ugettext_lazy('Product Name'), required=False)
    batch_number = forms.CharField(label=ugettext_lazy('Batch Number'), required=False)
    date_manufactured_from = forms.DateField(label=ugettext_lazy('From'), required=False)
    date_manufactured_to = forms.DateField(label=ugettext_lazy('To'), required=False)



    

