from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy


# Create your models here.

MINGUO = 1911

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

    class Meta:
        verbose_name = ugettext_lazy('Document')
        verbose_name_plural = ugettext_lazy('Document')
        
    def file_url(self):
        return self.file.url

    def __unicode__(self):
        return unicode(self.serial_number)

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

class BatchRecordInputForm(forms.ModelForm):
    date_manufactured = forms.DateField(label="Date of Manufacture")
    class Meta:
        model = BatchRecord

class BatchRecordSearchForm(forms.Form):
    name = forms.CharField(label=ugettext_lazy('Product Name'), required=False)
    batch_number = forms.CharField(label=ugettext_lazy('Batch Number'), required=False)
    date_manufactured_from = forms.DateField(label=ugettext_lazy('From'), required=False)
    date_manufactured_to = forms.DateField(label=ugettext_lazy('To'), required=False)


    

