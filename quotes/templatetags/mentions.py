from functools import partial
from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from ..regex import REGEX_SPEAKER, REGEX_REFERENCE

register = Library()

@register.filter(needs_autoescape = True)
@stringfilter
def mentions(text, autoescape = True):
    text = speakers(text, autoescape = autoescape)
    text = references(text, autoescape = autoescape)
    return text

@register.filter(needs_autoescape = True)
@stringfilter
def speakers(text, autoescape = True):
    if autoescape:
        escape = conditional_escape
    else:
        escape = lambda c: c

    return mark_safe(REGEX_SPEAKER.sub(partial(_replace_speaker, escape = escape), text))

@register.filter(needs_autoescape = True)
@stringfilter
def references(text, autoescape = True):
    if autoescape:
        escape = conditional_escape
    else:
        escape = lambda c: c

    # Replace escaped references with the @ entity.
    text = text.replace('\\@', '&comat;')

    text = REGEX_REFERENCE.sub(partial(_replace_reference, escape = escape), text)

    return mark_safe(text)

def _replace_speaker(match, escape = lambda c: c):
    (mention, ) = match.groups()
    try:
        speaker = User.objects.get(username = mention)
    except User.DoesNotExist:
        return match.string[match.start():match.end()]

    profile_url = reverse('user-profile', kwargs = {'username': speaker.username, })

    return '<strong><a class="text-primary" href="%s">%s</a>:</strong>' % (profile_url, escape(_resolve_name(speaker)), )

def _replace_reference(match, escape = lambda c: c):
    (previous_char, mention, ) = match.groups()

    try:
        reference = User.objects.get(username = mention)
    except User.DoesNotExist:
        return match.string[match.start():match.end()]

    profile_url = reverse('user-profile', kwargs = {'username': reference.username, })

    return '%s<strong><a class="text-muted" href="%s">%s</a></strong>' % (previous_char, profile_url, escape(_resolve_name(reference)), )

def _resolve_name(user):

    if user.get_short_name():
       return user.get_short_name()

    return user.username
