from django.contrib import admin
from django.utils.safestring import mark_safe
from app.models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админка для модели рецептов"""

    def get_ingredients_display(self, obj):
        ingredients = obj.recipe_ingredients.all()
        return mark_safe('<br>'.join([
            f'{ing.ingredient.name} - {ing.amount} {ing.ingredient.measurement_unit}'
            for ing in ingredients
        ]))
    get_ingredients_display.short_description = 'Продукты'

    def get_image_display(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return 'Нет изображения'
    get_image_display.short_description = 'Картинка'

    def get_favorites_count(self, obj):
        return obj.favorites.count()
    get_favorites_count.short_description = 'В избранном'

    list_display = (
        'id',
        'name',
        'cooking_time',
        'author',
        'get_favorites_count',
        'get_ingredients_display',
        'get_image_display',
    )
    search_fields = ('name', 'author__username', 'author__email')
    list_filter = ('author', 'created_at')
    ordering = ('id',) 