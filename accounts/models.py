from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    #Add other fields in the future
    
    class Meta:
        verbose_name = ugettext_lazy('User Profile')
        verbose_name_plural = ugettext_lazy('User Profiles')

    def __unicode__(self):
        return unicode(self.user)

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