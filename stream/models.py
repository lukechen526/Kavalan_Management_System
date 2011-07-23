from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver
import time

def calculate_rank(inst):

    #Convert both the time posted and current time to seconds since the Epoch time
    time_posted = int(time.mktime(inst.time_posted.timetuple()))
    current_time = int(time.time())

    #Calculates the rank, giving more weight to the current time (i.e. the time when the StreamPost is updated again).
    return int(0.7*current_time + 0.3*time_posted)


class StreamPost(models.Model):
    poster = models.ForeignKey(User, related_name='stream_posts', verbose_name=ugettext_lazy('Poster'))
    groups = models.ManyToManyField(Group, related_name='stream_posts', verbose_name=ugettext_lazy('Groups'))
    time_posted = models.DateTimeField(auto_now_add=True, verbose_name=ugettext_lazy('Time Posted'))
    content = models.TextField(blank=True, verbose_name=ugettext_lazy('Content'))
    link = models.URLField(blank=True, verbose_name=ugettext_lazy('Link'))
    rank = models.BigIntegerField(default=0, verbose_name=ugettext_lazy('Rank'))

    class Meta:
        ordering = ['-rank']

    def comment_count(self):
        return self.comments.count()

    def __unicode__(self):
        return unicode('%s %s %d' %(self.poster, self.time_posted, self.rank ))


class StreamPostComment(models.Model):
    poster = models.ForeignKey(User, verbose_name=ugettext_lazy('Poster'))
    stream_post = models.ForeignKey(StreamPost, related_name='comments', verbose_name=ugettext_lazy('Original Post'))
    time_posted = models.DateTimeField(auto_now_add=True, verbose_name=ugettext_lazy('Time Posted'))
    content = models.TextField(blank=True, verbose_name=ugettext_lazy('Content'))

    class Meta:
        ordering = ['-stream_post', 'time_posted']

@receiver(post_save, sender=StreamPost)
def update_rank(sender, **kwargs):
    """
    Updates the rank of a post after it is saved
    :param sender:
    :param kwargs:
    :return:
    """
    pk = kwargs['instance'].pk
    StreamPost.objects.filter(pk__exact=pk).update(rank=calculate_rank(kwargs['instance']))

@receiver(post_save, sender=StreamPostComment)
def update_stream_post_rank(sender, **kwargs):
    """
    After a comment is saved, re-saves the StreamPost it is associated with to update the rank
    :param sender:
    :param kwargs:
    :return:
    """
    stream_post = kwargs['instance'].stream_post
    stream_post.save()
    
