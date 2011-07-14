from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver

class MessageThread(models.Model):
    subject = models.CharField(max_length=200, verbose_name=ugettext_lazy('Thread Subject'))
    participants = models.ManyToManyField(User, verbose_name=ugettext_lazy('Participants'))
    last_updated = models.DateTimeField(auto_now=True, verbose_name=ugettext_lazy('Last Updated'))

    class Meta:
        verbose_name = ugettext_lazy('Message Thread')
        verbose_name_plural = ugettext_lazy('Message Threads')

    def __unicode__(self):
        return self.subject

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


@receiver(post_save, sender=Message)
def update_thread_time(sender, **kwargs):
    """
    Update the 'last_updated' field of of the message thread containing the new message
    :param sender:
    :param kwargs:
    :return:
    """
    kwargs['instance'].thread.save()

@receiver(post_save, sender=MessageThread)
def notify_user_thread_participation_or_update(sender, **kwargs):
    thread = kwargs['instance']
    is_new = kwargs['created']
    participants = thread.participants.all()

    if is_new:
        for participant in participants:
            participant.get_profile().notify(u"%s '%s'" %(ugettext_lazy("You have been added to"), thread.subject))
    else:
        for participant in participants:
            participant.get_profile().notify(u"%s '%s'" %(ugettext_lazy("New message in "), thread.subject))



