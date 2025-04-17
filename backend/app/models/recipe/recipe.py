from django.core.validators import MinValueValidator
from django.db import models
from ..user.user import User
from .ingredient import Ingredient


class Recipe(models.Model):
    """Модель рецептов"""

    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )

    text = models.TextField(
        verbose_name='Описание'
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
    )

    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/images/'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    cooking_time = models.IntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[
            MinValueValidator(
                1, 'Время приготовления не может быть менее 1 минуты'
            )
        ]
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-created_at',)
        default_related_name = 'recipes'

    def __str__(self):
        return f'ID рецепта: {self.id} | {self.name}'


class IngredientInRecipe(models.Model):
    """Промежуточная модель для связи рецептов с ингредиентами"""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )

    amount = models.IntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(
            1,
            'Количество ингредиента должно быть больше нуля!'
        )]
    )

    class Meta:
        verbose_name = 'Продукт рецепта'
        verbose_name_plural = 'Продукты рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]
        default_related_name = 'recipe_ingredients'

    def __str__(self):
        return f'{self.recipe.name} - {self.ingredient.name}'
