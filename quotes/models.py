from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.deconstruct import deconstructible
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db.models import Model
from django.db.models import DateTimeField, ForeignKey, CharField, TextField, ManyToManyField
from .regex import REGEX_SPEAKER, REGEX_REFERENCE

@deconstructible
class WordCountValidator(object):
    def __init__(self, min_count = 0, max_count = None):
        if max_count is not None and max_count < min_count:
            raise ValueError('min_count must be less than max_count')

        self.min_count = min_count
        self.max_count = max_count

    def __call__(self, value):
        word_count = sum(len(line.split(' ')) for line in value.splitlines())

        if word_count < self.min_count:
            raise ValidationError('Enter at least %d words' % (self.min_count, ))

        if self.max_count and self.max_count < word_count:
            raise ValidationError('Can\'t enter more than %d words' % (self.max_count, ))

@python_2_unicode_compatible
class Quote(Model):
    created = DateTimeField(auto_now_add = True)
    last_modified = DateTimeField(auto_now = True)
    author = ForeignKey(settings.AUTH_USER_MODEL, related_name = 'author_of')
    title = CharField(max_length = 120, blank = True)
    text = TextField(validators = [WordCountValidator(min_count = 2), ])
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
        for (speaker, _) in REGEX_SPEAKER.findall(self.text):
            try:
                self.mentions.add(get_user_model().objects.get(username = speaker))
            except get_user_model().DoesNotExist:
                # TODO: Log warning somewhere.
                pass

        # Mark referenced users as mentioned.
        for (_, reference, _) in REGEX_REFERENCE.findall(self.text):
            try:
                self.mentions.add(get_user_model().objects.get(username = reference))
            except get_user_model().DoesNotExist:
                # TODO: Log warning somewhere.
                pass

    class Meta:
        ordering = ('-created', )

class Comment(Model):
    created = DateTimeField(auto_now_add = True)
    last_modified = DateTimeField(auto_now = True)
    author = ForeignKey(settings.AUTH_USER_MODEL, related_name = 'comments')
    quote = ForeignKey(Quote, related_name = 'comments')
    text = TextField()
