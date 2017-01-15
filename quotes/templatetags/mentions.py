from __future__ import unicode_literals
from functools import partial
from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from profiles.templatetags.profiles import profile_link
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

    text = REGEX_SPEAKER.sub(
        partial(_replace_speaker, escape = escape),
        text)

    return mark_safe(text)

@register.filter(needs_autoescape = True)
@stringfilter
def references(text, autoescape = True):
    if autoescape:
        escape = conditional_escape
    else:
        escape = lambda c: c

    # Replace escaped references with the @ entity.
    text = text.replace('\\@', '&comat;')

    text = REGEX_REFERENCE.sub(
        partial(_replace_reference, escape = escape),
        text)

    return mark_safe(text)

def _replace_speaker(match, escape = lambda c: c):
    (mention, nickname, ) = match.groups()
    nickname = _fix_nickname(nickname)

    try:
        speaker = User.objects.get(username = mention)
    except User.DoesNotExist:
        return match.string[match.start():match.end()]

    link = profile_link(
        speaker,
        force_nickname = nickname,
        classes = 'text-primary')

    return '<strong>%s:</strong>' % (link, )

def _replace_reference(match, escape = lambda c: c):
    (previous_char, mention, nickname, ) = match.groups()
    nickname = _fix_nickname(nickname)

    try:
        reference = User.objects.get(username = mention)
    except User.DoesNotExist:
        return match.string[match.start():match.end()]

    link = profile_link(
        reference,
        force_nickname = nickname,
        classes = 'text-muted')

    return '%s<strong>%s</strong>' % (previous_char, link , )

def _fix_nickname(nickname):
    if not nickname:
        return None

    if nickname.startswith('"'):
        nickname = nickname[1:]
    if nickname.endswith('"'):
        nickname = nickname[:-1]

    return nickname
