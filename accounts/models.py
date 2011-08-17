from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy, activate
from django.conf import settings
import guess_language as gl
from notification import models as notification


LANGUAGES_CHOICES = settings.LANGUAGES

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    full_name = models.CharField(max_length=50)
    language = models.CharField(max_length=10, choices=LANGUAGES_CHOICES, default='en_us')
    
    class Meta:
        verbose_name = ugettext_lazy('User Profile')
        verbose_name_plural = ugettext_lazy('User Profiles')

    def __unicode__(self):
        return unicode(self.user)

    def unseen_notices(self):
        return notification.Notice.objects.notices_for(self.user, unseen=True)

@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):

    profile, new = UserProfile.objects.get_or_create(user=kwargs['instance'])
    
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