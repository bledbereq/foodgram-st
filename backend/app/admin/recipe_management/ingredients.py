from django.contrib import admin
from app.models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """
    Административная панель для управления ингредиентами.
    Предоставляет интерфейс для управления списком ингредиентов,
    используемых в рецептах.
    Attributes:
        list_display: Поля, отображаемые в списке ингредиентов
        list_filter: Поля для фильтрации ингредиентов
        search_fields: Поля, по которым можно осуществлять поиск
        ordering: Порядок сортировки ингредиентов
    """

    list_display = ('id', 'name', 'measurement_unit', 'get_recipe_count')
    list_filter = ('measurement_unit',)
    search_fields = ('name', 'measurement_unit')
    ordering = ('name',)

    def get_recipe_count(self, obj):
        """
        Подсчитывает количество рецептов, использующих данный ингредиент.
        Args:
            obj: Объект ингредиента
        Returns:
            Количество рецептов с данным ингредиентом
        """
        return obj.recipe_ingredients.count()
    get_recipe_count.short_description = 'Используется в рецептах'
