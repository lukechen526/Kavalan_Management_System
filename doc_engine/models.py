from django.db import models
from django import forms
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Document(models.Model):
    """
    Model for digitally stored documents
    
    - serial_number: CharField
    - title: CharField
    - author: CharField
    - version: CharField
    - file: FileField
    - last_updated: DateTimeField
    - permitted_groups: ManytoManyField

    """
    serial_number = models.CharField(max_length=50, unique='True', verbose_name=ugettext_lazy('Document Serial Number'))
    title = models.CharField(max_length=100, verbose_name=ugettext_lazy('Title'))
    author = models.CharField(max_length=100, default='Wufulab Ltd', verbose_name=ugettext_lazy('Author'))
    version = models.CharField(max_length=10, default='1.0', verbose_name=ugettext_lazy('Version'))
    file = models.FileField(upload_to='documents', verbose_name=ugettext_lazy('File'))
    last_updated = models.DateTimeField(verbose_name=ugettext_lazy('Last Updated'), auto_now=True)
    permitted_groups = models.ManyToManyField(Group, blank=True, verbose_name=ugettext_lazy('Permitted Groups'))

    class Meta:
        verbose_name = ugettext_lazy('Document')
        verbose_name_plural = ugettext_lazy('Documents')
        
    def file_url(self):
        return "/doc_engine/access/%s/" % self.pk

    def __unicode__(self):
        return unicode(u'%s %s v%s' %(self.serial_number, self.title, self.version))

@receiver(pre_delete, sender=Document)
def deleteFileOnServer(sender, **kwargs):
    """
    When a Document record is being removed, deletes the associated file from storage
    """
    document = kwargs['instance']
    document.file.delete()

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
        verbose_name_plural = ugettext_lazy('Batch Record')
        
    def __unicode__(self):
        return unicode(self.batch_number)

    def save(self, *args, **kwargs):
        if self.date_manufactured.year <= 1000:
            #Convert MINGUO Year to CE before saving
            self.date_manufactured = self.date_manufactured.replace(year=self.date_manufactured.year+MINGUO)
        super(BatchRecord, self).save(*args, **kwargs)

class BatchRecordInputForm(forms.ModelForm):
    date_manufactured = forms.DateField(label=ugettext_lazy('Date of Manufacture'))
    class Meta:
        model = BatchRecord

class BatchRecordSearchForm(forms.Form):
    name = forms.CharField(label=ugettext_lazy('Product Name'), required=False)
    batch_number = forms.CharField(label=ugettext_lazy('Batch Number'), required=False)
    date_manufactured_from = forms.DateField(label=ugettext_lazy('From'), required=False)
    date_manufactured_to = forms.DateField(label=ugettext_lazy('To'), required=False)



    

