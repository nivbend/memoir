from __future__ import unicode_literals
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.template import Library

register = Library()

@register.simple_tag
def profile_link(user, force_nickname = None, classes = None, escape = lambda c: c):
    if not classes:
        classes = ''

    attributes = [
        ('class', escape(classes)),
        ('href', user.profile.get_absolute_url()),
    ]

    return mark_safe(''.join([
        '<a %s>' % (_build_tag_attributes(attributes), ),
        escape(force_nickname if force_nickname else user.profile.get_name()),
        '</a>',
    ]))

@register.filter(needs_autoescape = True)
def profiles(users, autoescape = True):
    if autoescape:
        escape = conditional_escape
    else:
        escape = lambda c: c

    return [profile_link(user, escape = escape) for user in users]

@register.filter(is_safe = True)
def listify(items):
    if not items:
        return mark_safe('')

    if 1 == len(items):
        return items[0]

    return mark_safe(', '.join(items[:-1]) + ' and ' + items[-1])

def _build_tag_attributes(attributes):
    return ' '.join('%s="%s"' % (attribute, value, ) for (attribute, value) in attributes)
