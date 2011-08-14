from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy
import guess_language as gl

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    full_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = ugettext_lazy('User Profile')
        verbose_name_plural = ugettext_lazy('User Profiles')

    def __unicode__(self):
        return unicode(self.user)

@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if kwargs['created']:
        profile = UserProfile(user=kwargs['instance'])
    else:
        profile = UserProfile.objects.get(user__pk__exact=kwargs['instance'].pk)
    
     #Figure out the correct format for the full name based on the language
    s = u'%s%s' % (profile.user.first_name, profile.user.last_name)
    lang = gl.guessLanguage(s)
    if lang == 'zh':
        profile.full_name = u'%s%s' % (profile.user.last_name, profile.user.first_name)
    else:
        profile.full_name = u'%s %s' % (profile.user.first_name, profile.user.last_name)
    profile.save()

class CustomUserCreationForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), label=ugettext_lazy('Groups'))