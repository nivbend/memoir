from __future__ import unicode_literals
from django.contrib.admin import ModelAdmin, register
from .models import Board, Quote, Comment

@register(Board)
class BoardAdmin(ModelAdmin):
    pass

@register(Quote)
class QuoteAdmin(ModelAdmin):
    pass

@register(Comment)
class CommentAdmin(ModelAdmin):
    pass
