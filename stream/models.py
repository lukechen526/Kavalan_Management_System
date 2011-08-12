from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy, ugettext
from django.db.models.signals import post_save
from django.dispatch import receiver
import time, datetime
import cgi

def calculate_rank(inst):

    #Convert both the time posted and current time to seconds since the Epoch time.
    #Rank = 0.7*(the time of rank calculation in seconds since the Epoch time) + 0.3*(the time of posting in seconds since the Epoch time)

    try:
        time_posted = int(time.mktime(inst.time_posted.timetuple()))
    except AttributeError:
        time_posted = int(time.mktime(datetime.datetime.now().timetuple()))
    current_time = int(time.time())
    
    #Calculates the rank, giving more weight to the current time (i.e. the time when the StreamPost is updated again).
    return int(0.7*current_time + 0.3*time_posted)


class StreamPost(models.Model):
    """
    Model for posts in the Stream.

    - poster: ForeignKey to User
    - groups: ManyToManyField to Group
    - time_posted: DateTimeField, auto_now_add=True
    - content: TextField, blank=True
    - link: URLField, blank=True
    - rank: BigIntegerField
    
    """
    poster = models.ForeignKey(User, related_name='stream_posts', verbose_name=ugettext_lazy('Poster'))
    groups = models.ManyToManyField(Group, related_name='stream_posts', verbose_name=ugettext_lazy('Groups'))
    time_posted = models.DateTimeField(auto_now_add=True, verbose_name=ugettext_lazy('Time Posted'))
    content = models.TextField(blank=True, verbose_name=ugettext_lazy('Content'))
    link = models.URLField(blank=True, verbose_name=ugettext_lazy('Link'))
    rank = models.BigIntegerField(default=0, verbose_name=ugettext_lazy('Rank'))

    class Meta:
        ordering = ['-rank']

    def __unicode__(self):
        return unicode('%s %s %d' %(self.poster, self.time_posted, self.rank ))

    def save(self, *args, **kwargs):
        self.rank = calculate_rank(self)
        super(StreamPost, self).save(*args, **kwargs)
        
    def comment_count(self):
        return self.comments.count()

    def processed_content(self):
        return unicode(cgi.escape(self.content))

    def formatted_time_posted(self):
        """
        Formats the time of posting into more human-readable form, e.g. "4 minutes ago", "3 days ago".
        """
        now = datetime.datetime.now()
        diff = now - self.time_posted

        if diff.days > 0:
            if diff.days == 1:
                return unicode('%d %s' %(1, ugettext('day ago') ))
            else:
                return unicode('%d %s' %(diff.days, ugettext('days ago') ))

        if diff.seconds >= 60*60: #if the post was posted no less than an hour but less than a day ago
            if diff.seconds < 2 * 60* 60:
                return unicode('%d %s' %(1, ugettext('hour ago') ))
            else:
                return unicode('%d %s' %(int(diff.seconds/3600), ugettext('hours ago') ))

        if diff.seconds >= 60: #if the post was posted no less than a minute but less than an hour ago
            if diff.seconds < 2 * 60:
                return unicode('%d %s' %(1, ugettext('minute ago') ))
            else:
                return unicode('%d %s' %(int(diff.seconds/60), ugettext('minutes ago') ))
        else:
            if diff.seconds <= 1:
                return unicode('%d %s' %(1, ugettext('second ago') ))
            else:
                return unicode('%d %s' %(diff.seconds, ugettext('seconds ago') ))

class StreamPostValidationForm(ModelForm):
    class Meta:
        model = StreamPost
        fields = ('groups', 'content', 'link')

class StreamPostComment(models.Model):
    poster = models.ForeignKey(User, verbose_name=ugettext_lazy('Poster'))
    stream_post = models.ForeignKey(StreamPost, related_name='comments', verbose_name=ugettext_lazy('Original Post'))
    time_posted = models.DateTimeField(auto_now_add=True, verbose_name=ugettext_lazy('Time Posted'))
    content = models.TextField(verbose_name=ugettext_lazy('Content'))

    class Meta:
        ordering = ['-stream_post', 'time_posted']

    def processed_content(self):
        return unicode(cgi.escape(self.content))

    def formatted_time_posted(self):
        now = datetime.datetime.now()
        diff = now - self.time_posted
        
        if diff.days > 0:
            if diff.days == 1:
                return unicode('%d %s' %(1, ugettext('day ago') ))
            else:
                return unicode('%d %s' %(diff.days, ugettext('days ago') ))

        if diff.seconds >= 60*60: #if the post was posted no less than an hour but less than a day ago
            if diff.seconds < 2 * 60* 60:
                return unicode('%d %s' %(1, ugettext('hour ago') ))
            else:
                return unicode('%d %s' %(int(diff.seconds/3600), ugettext('hours ago') ))

        if diff.seconds >= 60: #if the post was posted no less than a minute but less than an hour ago
            if diff.seconds < 2 * 60:
                return unicode('%d %s' %(1, ugettext('minute ago') ))
            else:
                return unicode('%d %s' %(int(diff.seconds/60), ugettext('minutes ago') ))
        else:
            if diff.seconds <= 1:
                return unicode('%d %s' %(1, ugettext('second ago') ))
            else:
                return unicode('%d %s' %(diff.seconds, ugettext('seconds ago') ))


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
    
class StreamPostCommentValidationForm(ModelForm):
    class Meta:
        model = StreamPostComment
        fields = ('content',)