from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from recipe.models import Recipe, Ingredient_In_Recipe
from .user import Author_Serializer
from .ingredient import Ingredient_Serializer

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

class Recipe_Serializer(serializers.ModelSerializer):
    author = Author_Serializer(read_only=True)
    ingredients = Ingredient_Serializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return request.user.favorites.filter(pk=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return request.user.in_cart.filter(pk=obj.id).exists()

    def create_ingredients(self, ingredient_list, recipe):
        Ingredient_In_Recipe.objects.bulk_create(
            Ingredient_In_Recipe(
                ingredient_id=i.get("id"),
                recipe=recipe,
                amount=i.get("amount")
            )
            for i in ingredient_list
        )

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(
            **validated_data,
            author=self.context.get("request").user
        )
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        Ingredient_In_Recipe.objects.filter(recipe=instance.id).delete()
        self.create_ingredients(validated_data.pop("ingredients"), instance)
        return super().update(instance, validated_data) 