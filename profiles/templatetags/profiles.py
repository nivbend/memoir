from django.core.urlresolvers import reverse
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.template import Library

register = Library()

@register.simple_tag
def profile_link(user, classes = '', escape = lambda c: c):
    profile_url = reverse('user-profile', kwargs = {'username': user.username, })

    return mark_safe(''.join([
        '<a class="%s" href="%s">' % (escape(classes), profile_url, ),
        escape(_resolve_name(user)),
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

def _resolve_name(user):
    if user.profile.nickname:
        return user.profile.nickname

    if user.get_short_name():
       return user.get_short_name()

    return user.username
