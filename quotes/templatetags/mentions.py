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
    text = references(text, autoescape = autoescape)
    text = speakers(text, autoescape = autoescape)
    return text

@register.filter(needs_autoescape = True)
@stringfilter
def speakers(text, autoescape = True):
    if autoescape:
        escape = conditional_escape
    else:
        escape = lambda c: c

    for line in text.splitlines():
        match = REGEX_SPEAKER.match(line)
        if match:
            (mention, nickname, text) = match.groups()
            nickname = _fix_nickname(nickname)
            if nickname:
                nickname = nickname.replace(' ', '&nbsp;')

            try:
                speaker = User.objects.get(username = mention)
            except User.DoesNotExist:
                yield (None, None, mark_safe(line))

            yield (speaker, nickname, mark_safe(text))
        else:
            yield (None, None, mark_safe(line))

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

def _replace_reference(match, escape = lambda c: c):
    (previous_char, mention, nickname) = match.groups()
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
