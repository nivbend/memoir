from __future__ import unicode_literals
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_auth_ldap.backend import populate_user
from .models import UserProfile

try:
    USER_ATTR_IMAGE_URL = settings.AUTH_LDAP_USER_ATTR_IMAGE_URL
except AttributeError:
    USER_ATTR_IMAGE_URL = None

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)

@receiver(populate_user)
def populate_profile(sender, user, ldap_user, **kwargs):
    if USER_ATTR_IMAGE_URL is None:
        return

    (user.profile.image_url, ) = ldap_user.attrs.get(USER_ATTR_IMAGE_URL, ('', ))
    user.profile.save()
