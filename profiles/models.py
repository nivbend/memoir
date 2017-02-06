from __future__ import unicode_literals
from operator import or_
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.db.models import Model, CASCADE
from django.db.models import OneToOneField, CharField

@python_2_unicode_compatible
class UserProfile(Model):
    user = OneToOneField(settings.AUTH_USER_MODEL, on_delete = CASCADE, related_name = 'profile')
    nickname = CharField(max_length = 20, blank = True)

    @property
    def boards(self):
        return reduce(or_, (g.boards.all() for g in self.user.groups.all())).distinct()

    @property
    def quotes(self):
        return self.user.author_of.all()

    @property
    def mentions(self):
        return self.user.mentioned_in.all()

    def get_name(self):
        if self.nickname:
            return self.nickname

        if self.user.get_short_name():
            return self.user.get_short_name()

        return self.user.username

    def get_absolute_url(self):
        return reverse('user-profile', kwargs = {'username': self.user.username, })

    def __str__(self):
        return '%s\'s profile' % (self.user, )

    def save(self, *args, **kwargs):
        # This fixes an issue when creating a new user with the admin interface,
        # each inline form triggers a new save, and since the profile wasn't committed to
        # the database yet (has no pk), a new UserProfile is created, which violates the
        # UNIQUE constraint.
        # Instead, we lookup for an existing profile belonging to the user and cause
        # an update instead of a create.
        if not self.pk:
            try:
                current_profile = UserProfile.objects.get(user = self.user)
                self.pk = current_profile.pk
            except UserProfile.DoesNotExist:
                pass

        super(UserProfile, self).save(*args, **kwargs)
