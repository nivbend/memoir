from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db.models import Model, SET_NULL
from django.db.models import DateTimeField, ForeignKey, CharField, TextField, ManyToManyField
from .regex import REGEX_SPEAKER, REGEX_REFERENCE

@python_2_unicode_compatible
class Quote(Model):
    created = DateTimeField(auto_now_add = True)
    last_modified = DateTimeField(auto_now = True)
    author = ForeignKey(settings.AUTH_USER_MODEL, related_name = 'author_of')
    title = CharField(max_length = 120, blank = True)
    text = TextField()
    mentions = ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank = True,
        editable = False,
        related_name = 'mentioned_in')
    likers = ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank = True,
        editable = False,
        related_name = 'likes')

    def __str__(self):
        if self.title:
            return self.title
        if self.id:
            return '#%d' % (self.id, )
        return 'Quote object'

    def save(self, *args, **kws):
        super(Quote, self).save(*args, **kws)
        self.__update_mentions()

    def get_absolute_url(self):
        return reverse('quote:detail', kwargs = {'pk': self.pk, })

    def __update_mentions(self):
        self.mentions.clear()

        # Mark speakers as mentioned.
        for speaker in REGEX_SPEAKER.findall(self.text):
            try:
                self.mentions.add(get_user_model().objects.get(username = speaker))
            except get_user_model().DoesNotExist:
                # TODO: Log warning somewhere.
                pass

        # Mark referenced users as mentioned.
        for (_, reference) in REGEX_REFERENCE.findall(self.text):
            try:
                self.mentions.add(get_user_model().objects.get(username = reference))
            except get_user_model().DoesNotExist:
                # TODO: Log warning somewhere.
                pass

    class Meta:
        ordering = ('-created', )
