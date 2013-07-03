from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import permalink
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from allauth.socialaccount.signals import social_account_added

class Profile(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    about = models.CharField(max_length=140)
    photo = models.ImageField(upload_to='profiles', blank=True, null=True)
    is_public = models.BooleanField(default=True)

    @property
    def full_name(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name)
        
    def __unicode__(self):
        if self.user.first_name:
            return u'%s' % self.full_name
        else:
            return u'%s' % self.user.username

    def get_absolute_url(self):
        kwargs = {"username": self.user.username}
        return reverse("profile_detail", kwargs=kwargs)

@receiver(post_save, sender=User)
def user_post_save(sender, **kwargs):
    """
    Create a Profile instance for all newly created User instances.
    Run only on user creation to avoid having to check for existence
    on each call to User.save
    """
    user, created = kwargs["instance"], kwargs["created"]
    if created:
        Profile.objects.create(user=user)

@receiver(social_account_added)
def populate_profile(sender, **kwargs):
    pass
    #u = UserProfile( >>FACEBOOK_DATA<< )
    #u.save()
