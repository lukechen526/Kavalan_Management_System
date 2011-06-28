from django.db import models
from django.utils.translation import ugettext_lazy
from django.forms import ModelForm

# Create your models here.
class Document(models.Model):
    serial_number = models.CharField(max_length=50, unique='True', verbose_name=ugettext_lazy('Document Serial Number'))
    title = models.CharField(max_length=100, verbose_name=ugettext_lazy('Title'))
    author = models.CharField(max_length=100, default='Wufulab Ltd', verbose_name=ugettext_lazy('Author'))
    version = models.IntegerField(verbose_name=ugettext_lazy('Version'))
    file = models.FileField(upload_to='documents', verbose_name=ugettext_lazy('File'))
    last_updated = models.DateTimeField(verbose_name=ugettext_lazy('Last Updated'), auto_now=True)
    
    class Meta:
        verbose_name = ugettext_lazy('Document')

    def __unicode__(self):
        return self.serial_number

        