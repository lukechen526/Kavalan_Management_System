from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    department = models.CharField(max_length=50, default="General", verbose_name=ugettext_lazy("Department"))

    class Meta:
        verbose_name = ugettext_lazy("User Profile")
        verbose_name_plural = ugettext_lazy("User Profile")

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
