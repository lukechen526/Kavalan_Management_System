from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

class MessageThread(models.Model):
    subject = models.CharField(max_length=200, verbose_name=ugettext_lazy('Thread Subject'))
    creator = models.ForeignKey(User)
    participants = models.ManyToManyField(User, through='ThreadParticipation', related_name='threads_participated', verbose_name=ugettext_lazy('Participants'))
    owners = models.ManyToManyField(User, through='ThreadOwnership', related_name='threads_owned', verbose_name=ugettext_lazy('Owners'))
    last_updated = models.DateTimeField(auto_now=True, verbose_name=ugettext_lazy('Last Updated'))

    class Meta:
        verbose_name = ugettext_lazy('Message Thread')
        verbose_name_plural = ugettext_lazy('Message Threads')

    def __unicode__(self):
        return unicode(self.id)

class Message(models.Model):
    poster = models.ForeignKey(User, verbose_name=ugettext_lazy('Poster'))
    date_time = models.DateTimeField(auto_now=True, verbose_name=ugettext_lazy('Date'))
    content = models.TextField(default='', verbose_name=ugettext_lazy('Content'))
    thread = models.ForeignKey(MessageThread, verbose_name=ugettext_lazy('Thread'))

    class Meta:
        verbose_name = ugettext_lazy('Message')
        verbose_name_plural = ugettext_lazy('Messages')

    def __unicode__(self):
        return unicode(self.id)

class ThreadParticipation(models.Model):
    participant = models.ForeignKey(User)
    thread = models.ForeignKey(MessageThread)
    last_updated = models.DateTimeField(auto_now=True, verbose_name=ugettext_lazy('Last Updated'))
    unread = models.BooleanField(default=True, verbose_name=ugettext_lazy('Unread'))

class ThreadOwnership(models.Model):
    owner = models.ForeignKey(User)
    thread = models.ForeignKey(MessageThread)
    date_added = models.DateTimeField(auto_now_add=True)


    
class Notification(models.Model):
    time = models.TimeField(auto_now=True)
    content = models.CharField(max_length=200, default="Default Notification", verbose_name=ugettext_lazy('Content'))
    STATUS_CHOICES = (
        ('UNREAD', ugettext_lazy('unread')),
        ('READ', ugettext_lazy('read'))
    )
    status = models.CharField(max_length=10, default='UNREAD',choices=STATUS_CHOICES, verbose_name=ugettext_lazy('Status'))

    class Meta:
        verbose_name = ugettext_lazy('Notification')
        verbose_name_plural = ugettext_lazy('Notifications')

    def __unicode__(self):
        return self.content


@receiver(post_save, sender=Message)
def update_thread_time(sender, **kwargs):
    """
    Update the 'last_updated' field of of the message thread containing the new message
    :param sender:
    :param kwargs:
    :return:
    """
    kwargs['instance'].thread.save()


class NonceValue(models.Model):
    value = models.CharField(max_length=30, default='0')

class UserHAuthParameters(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=30, default="0")
    secret = models.CharField(max_length=30, default="0")
    last_timestamp = models.CharField(max_length=15, default='0')
    nonces = models.ManyToManyField(NonceValue)

    def check_duplicate_nonce(self, nonce_value):
        return self.nonces.filter(value__exact=nonce_value).exists()

    def clear_all_nonces(self):
        nonces = self.nonces.all()
        self.nonces.clear()
        nonces.delete()

    def add_nonce(self, nonce_value):
        nonce = NonceValue.objects.create(value=nonce_value)
        self.nonces.add(nonce)
        self.save()
        

        

            

    