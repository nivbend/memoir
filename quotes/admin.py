from django.contrib.admin import ModelAdmin, register
from .models import Quote

@register(Quote)
class QuoteAdmin(ModelAdmin):
    pass
