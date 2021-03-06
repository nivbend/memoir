from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.template import Library

register = Library()

@register.inclusion_tag('quotes/parts/user_buttons.html', takes_context = True)
def user_buttons(context):
    quote = context['quote']

    return {
        'edit_url': reverse('board:quote:edit', kwargs = {'board': quote.board.slug, 'pk': quote.pk, }),
        'delete_modal_id': 'delete_modal_%d' % (quote.pk, ),
    }

@register.inclusion_tag('quotes/parts/title.html', takes_context = True)
def quote_title(context):
    quote = context['quote']
    with_link = context.get('with_link', True)

    detail_url = ''
    if with_link:
        detail_url = reverse('board:quote:detail', kwargs = {'board': quote.board.slug, 'pk': quote.pk, })

    return {
        'quote_title': str(quote),
        'detail_url': detail_url,
    }

@register.inclusion_tag('quotes/parts/body.html', takes_context = True)
def quote_body(context):
    return {'quote_text': context['quote'].text, }

@register.inclusion_tag('quotes/parts/delete_modal.html', takes_context = True)
def delete_modal(context):
    quote = context['quote']

    return {
        'delete_modal_id': 'delete_modal_%d' % (quote.id, ),
        'delete_url': reverse('board:quote:delete', kwargs = {'board': quote.board.slug, 'pk': quote.pk, }),
    }

@register.inclusion_tag('quotes/parts/comments.html', takes_context = True)
def comments(context):
    quote = context['quote']

    return {
        'board': quote.board,
        'quote_pk': quote.pk,
        'comments': quote.comments.all(),
        'user': context['user'],
    }
