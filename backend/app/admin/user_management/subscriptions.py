from django.contrib import admin
from app.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Админка для модели подписок"""
    list_display = ('user', 'author')
    search_fields = ('user__email', 'author__email')
    list_filter = ('user', 'author') 