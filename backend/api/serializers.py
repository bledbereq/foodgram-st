from rest_framework import serializers
from recipe.models import Ingredient, Ingredient_In_Recipe
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from recipe.models import Recipe
from auth.models import Subscribe

class Ingredient_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "meas_unit")
        read_only_fields = ("id", "name", "meas_unit")

class Ingredient_Recipe_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient_In_Recipe
        fields = ("id", "name", "meas_unit", "amount")

class Author_Serializer(serializers.ModelSerializer):
    avatar = Base64ImageField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "username", "first_name", "last_name", "avatar", "is_subscribed")

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.subscribers.filter(id=request.user.id).exists()

class Subscriber_Serializer(Author_Serializer):
    recipes = serializers.SerializerMethodField(method_name="get_recipes")
    recipes_count = serializers.IntegerField(source="recipes.count")

    class Meta:
        model = get_user_model()
        fields = (
            "id", "email", "username", "first_name", "last_name",
            "recipes", "recipes_count"
        )

    def get_recipes(self, obj):
        request = self.context.get("request")
        recipes_limit = request.query_params.get("recipes_limit")
        recipes = obj.recipes.all()[:int(recipes_limit)] if recipes_limit else obj.recipes.all()
        return Short_Recipe_Serializer(
            recipes, context={"request": request}, many=True
        ).data

class Subscription_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = (
            "subscribing_user", "target"
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