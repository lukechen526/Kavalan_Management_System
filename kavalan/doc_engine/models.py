from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy

class Tag(models.Model):
    tag = models.SlugField(default='')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = ugettext_lazy('Tag')
        verbose_name_plural = ugettext_lazy('Tags')

    def __unicode__(self):
        return self.tag

class AccessRecord(models.Model):
    """
    Model for recording the access of any item by any user

    """
    user = models.ForeignKey(User, verbose_name=ugettext_lazy('User') )
    access_time = models.DateTimeField(auto_now_add=True, verbose_name=ugettext_lazy('Access Time'))
    ip = models.IPAddressField(verbose_name=ugettext_lazy('IP'))
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    item_accessed = generic.GenericForeignKey('content_type', 'object_id')
    success = models.BooleanField()

    class Meta:
        verbose_name = ugettext_lazy('Access Record')
        verbose_name_plural = ugettext_lazy('Access Records')
        permissions = (
            ("view_accessrecord", "Can view but not add/change/delete records"),
        )
        ordering = ['-access_time', 'user']

    def __unicode__(self):
        if self.success:
            return u"%s: %s %s %s" %(ugettext_lazy('SUCCESS'),self.user, self.item_accessed, self.access_time.isoformat(' '))
        else:
            return u"%s: %s %s %s" %(ugettext_lazy('FAILURE'),self.user, self.item_accessed, self.access_time.isoformat(' '))


class BaseDocument(models.Model):
    """
    The abstract base class of all document-like models

    - name
    - last_update
    - file
    - comment
    - tags

    """
    name = models.CharField(max_length=100, verbose_name=ugettext_lazy('Name'))
    date_modified = models.DateTimeField(verbose_name=ugettext_lazy('Date Modified'), auto_now=True)
    file = models.FileField(upload_to='doc_engine', verbose_name=ugettext_lazy('File'), null=True, blank=True)
    comment = models.TextField(default='', verbose_name=ugettext_lazy('Comment'), blank=True)
    tags = generic.GenericRelation(Tag, related_name='%(app_label)s_%(class)s_related')

    class Meta:
        abstract = True
        ordering = ['name', '-date_modified']

    def __unicode__(self):
        return self.name


class StoredDocumentManager(models.Manager):

    def get_by_natural_key(self, name, serial_number):
        return self.get(name=name, serial_number=serial_number)

class StoredDocument(BaseDocument):
    """
    The model for representing digitally stored copies of documents.
    """

    objects = StoredDocumentManager()

    serial_number = models.CharField(max_length=50, unique='True', verbose_name=ugettext_lazy('Document Serial Number'))
    location = models.CharField(max_length=30, default='', verbose_name=ugettext_lazy('Physical Location'))
    permitted_groups = models.ManyToManyField(Group, blank=True, verbose_name=ugettext_lazy('Permitted Groups'))
    access_records = generic.GenericRelation('AccessRecord')

    DOCUMENT_LEVELS = (
        ('1', ugettext_lazy('Level 1')),
        ('2', ugettext_lazy('Level 2')),
        ('3', ugettext_lazy('Level 3')),
        ('4', ugettext_lazy('Level 4')),
        )
    document_level = models.CharField(max_length=1, default='4',choices=DOCUMENT_LEVELS, verbose_name=ugettext_lazy('Document Level'))

    class Meta(BaseDocument.Meta):
        verbose_name = ugettext_lazy('Stored Document')
        verbose_name_plural = ugettext_lazy('Stored Documents')

        unique_together = ('name', 'serial_number')

    def __unicode__(self):
        return u'%s %s' %(self.name, self.serial_number)

    def natural_key(self):
        return (self.name, self.serial_number)

    def display_tags(self):
        span_list = []

        for tag in self.tags.all():
            span_list.append('<span style="display: inline-block; background-color: #DACFE8; padding: 0 2px;">%s</span>' % (tag.tag,))
        return ' '.join(span_list)
    
    display_tags.allow_tags = True
    display_tags.short_description = ugettext_lazy('Tag')



class BatchRecord(BaseDocument):
    """
    Model for batch records

    - name: CharField
    - batch_number: CharField
    - serial_number: IntegerField
    - date_of_manufacture: DateField
    - location: CharField

    """
    batch_number = models.CharField(max_length=30, verbose_name=ugettext_lazy('Batch Number'))
    serial_number = models.IntegerField(verbose_name=ugettext_lazy('Serial Number'))
    date_of_manufacture = models.DateField(auto_created=True, verbose_name=ugettext_lazy('Date of Manufacture'))
    location = models.CharField(max_length=30, verbose_name=ugettext_lazy('Physical Location'))

    class Meta:
        verbose_name = ugettext_lazy('Batch Record')
        verbose_name_plural = ugettext_lazy('Batch Records')
        
    def __unicode__(self):
        return self.batch_number

    def date_of_manufacture_in_minguo(self):
        return self.date_of_manufacture.replace(year=self.date_of_manufacture.year-1911)


    

