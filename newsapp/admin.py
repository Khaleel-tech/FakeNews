from django.contrib import admin

from .models import NewsCheck


@admin.register(NewsCheck)
class NewsCheckAdmin(admin.ModelAdmin):
    list_display = ('headline', 'classification', 'score', 'source_reference', 'created_at')
    list_filter = ('classification', 'source_reference', 'created_at')
    search_fields = ('headline', 'content')
