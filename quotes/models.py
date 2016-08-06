from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Model
from django.db.models import DateTimeField, ForeignKey, CharField, TextField

@python_2_unicode_compatible
class Quote(Model):
    created = DateTimeField(auto_now_add = True)
    last_modified = DateTimeField(auto_now = True)
    author = ForeignKey(settings.AUTH_USER_MODEL)
    title = CharField(max_length = 120, blank = True)
    text = TextField()

    def __str__(self):
        if self.title:
            return self.title
        if self.id:
            return '#%d' % (self.id, )
        return 'Quote object'

    def get_absolute_url(self):
        return reverse('quote:detail', kwargs = {'pk': self.pk, })
