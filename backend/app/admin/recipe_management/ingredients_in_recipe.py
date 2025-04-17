from django.contrib import admin
from app.models import IngredientInRecipe


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    """Админка для промежуточной модели ингредиентов в рецепте"""

    list_display = ('recipe', 'ingredient', 'amount')
    search_fields = ('recipe__name', 'ingredient__name') 