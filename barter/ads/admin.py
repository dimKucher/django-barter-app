from django.contrib import admin

from ads.models import AdsItem


@admin.register(AdsItem)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'condition', 'created_at', 'updated_at')
    list_filter = ('category', 'condition', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
