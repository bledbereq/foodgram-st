from django.contrib import admin
from app.models import Favorite, ShoppingCart


@admin.register(Favorite, ShoppingCart)
class FavoriteAndShoppingCartAdmin(admin.ModelAdmin):
    """
    Административная панель для управления избранным и корзиной покупок.
    Предоставляет интерфейс для управления списками избранных рецептов
    и рецептов в корзине покупок пользователей.
    Attributes:
        list_display: Поля, отображаемые в списке записей
        search_fields: Поля, по которым можно осуществлять поиск
        list_filter: Поля для фильтрации записей
        ordering: Порядок сортировки записей
    """

    def get_model_name(self, obj):
        """
        Определяет тип записи (избранное или корзина покупок).
        Args:
            obj: Объект записи
        Returns:
            Название модели, к которой относится запись
        """
        return 'Избранное' if isinstance(obj, Favorite) else 'Корзина покупок'
    get_model_name.short_description = 'Тип'

    list_display = ('id', 'user', 'recipe', 'get_model_name', 'created_at')
    search_fields = ('user__email', 'user__username', 'recipe__name')
    list_filter = ('user', 'recipe__author')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
