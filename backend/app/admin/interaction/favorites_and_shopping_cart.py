from django.contrib import admin
from app.models import Favorite, ShoppingCart


@admin.register(Favorite, ShoppingCart)
class FavoriteAndShoppingCartAdmin(admin.ModelAdmin):
    """Админка для моделей избранного и списка покупок"""
    list_display = ('user', 'recipe')
    search_fields = ('user__email', 'recipe__name')
    list_filter = ('user',) 