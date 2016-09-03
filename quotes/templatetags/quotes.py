from django.core.urlresolvers import reverse
from django.template import Library

register = Library()

@register.inclusion_tag('quotes/quote/user_buttons.html', takes_context = True)
def user_buttons(context):
    quote = context['quote']

    return {
        'edit_url': reverse('quote:edit', kwargs = {'pk': quote.pk, }),
        'delete_modal_id': 'delete_modal_%d' % (quote.pk, ),
    }

@register.inclusion_tag('quotes/quote/title.html', takes_context = True)
def quote_title(context):
    quote = context['quote']
    with_link = context.get('with_link', True)

    detail_url = ''
    if with_link:
        detail_url = reverse('quote:detail', kwargs = {'pk': quote.pk, })

    return {
        'quote_title': str(quote),
        'detail_url': detail_url,
    }

@register.inclusion_tag('quotes/quote/body.html', takes_context = True)
def quote_body(context):
    return {'quote_text': context['quote'].text, }

@register.inclusion_tag('quotes/quote/delete_modal.html', takes_context = True)
def delete_modal(context):
    quote = context['quote']

    return {
        'delete_modal_id': 'delete_modal_%d' % (quote.id, ),
        'delete_url': reverse('quote:delete', kwargs = {'pk': quote.pk, }),
    }

@register.inclusion_tag('quotes/quote/comments.html', takes_context = True)
def comments(context):
    quote = context['quote']

    return {
        'quote_pk': quote.pk,
        'comments': quote.comments.all(),
        'user': context['user'],
    }
