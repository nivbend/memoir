from django.core.urlresolvers import reverse
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

def _resolve_name(user):
    if user.profile.nickname:
        return user.profile.nickname

    if user.get_short_name():
       return user.get_short_name()

    return user.username
