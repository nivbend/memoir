from __future__ import unicode_literals
from django.contrib.admin import ModelAdmin, register
from .models import Quote, Comment

@register(Quote)
class QuoteAdmin(ModelAdmin):
    pass

@register(Comment)
class CommentAdmin(ModelAdmin):
    pass
