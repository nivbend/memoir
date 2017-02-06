from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.template import Library

register = Library()

@register.inclusion_tag('quotes/like_button.html', takes_context = True)
def like_button(context):
    quote = context['quote']

    button_classes = 'btn btn-default btn-like'
    if quote.likers.filter(pk = context['user'].pk).exists():
        button_classes = 'btn btn-primary btn-unlike'

    return {
        'classes': button_classes,
        'button_id': 'like_%d' % (quote.pk, ),
        'url': reverse('board:quote:like', kwargs = {'board': quote.board.slug, 'pk': quote.pk, }),
        'count': quote.likers.count(),
    }
