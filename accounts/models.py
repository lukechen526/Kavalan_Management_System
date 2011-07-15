from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy


# Create your models here.
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
    
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    department = models.CharField(max_length=50, default='General', verbose_name=ugettext_lazy('Department'))
    notifications = models.ManyToManyField(Notification, blank=True, verbose_name=ugettext_lazy('Notifications'))
    new_notification_count = models.IntegerField(default=0, verbose_name=ugettext_lazy('New Notification Count'))

    class Meta:
        verbose_name = ugettext_lazy('User Profile')
        verbose_name_plural = ugettext_lazy('User Profiles')

    def __unicode__(self):
        return unicode(self.user)

    def notify(self, content):
        self.notifications.create(content=content)
        self.new_notification_count += 1
        self.save()

@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if kwargs['created']:
        profile = UserProfile(user=kwargs['instance'])
        profile.save()
    else:
        profile = UserProfile.objects.get(user__pk__exact=kwargs['instance'].pk)
        profile.save()


        
class CustomUserCreationForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), label=ugettext_lazy('Groups'))