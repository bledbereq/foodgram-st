from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from recipe.models import Recipe, Ingredient, Ingredient_In_Recipe

class Short_Recipe_Serializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')

class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='ingredient.id', read_only=True)
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit', read_only=True)

    class Meta:
        model = Ingredient_In_Recipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    ingredients = serializers.ListField(
        child=serializers.DictField(),
        write_only=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text', 'ingredients', 'cooking_time', 'created_at')

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            ingredient, _ = Ingredient.objects.get_or_create(
                name=ingredient_data['name'],
                measurement_unit=ingredient_data['measurement_unit']
            )
            Ingredient_In_Recipe.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=ingredient_data['amount']
            )

        return recipe

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ingredients'] = IngredientInRecipeSerializer(
            instance.recipe_ingredients.all(), many=True
        ).data
        return representation 