from django.contrib import admin
from .models import Source, Quote, AppStat

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'created_at')
    search_fields = ('name',)
    list_filter = ('type',)

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'source', 'weight', 'likes', 'dislikes', 'views', 'created_at')
    list_filter = ('source__type',)
    search_fields = ('text', 'source__name')

    def short_text(self, obj):
        return (obj.text[:80] + '…') if len(obj.text) > 80 else obj.text

@admin.register(AppStat)
class AppStatAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
