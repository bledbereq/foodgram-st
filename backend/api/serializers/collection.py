from rest_framework import serializers
from auth.models import Subscribe
from recipe.models import User_Favorite, User_Cart
from .recipe import Short_Recipe_Serializer

class Subscription_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = (
            "subscribing_user", "target"
        )

class Recipe_Collection_Serializer(serializers.Serializer):
    class Meta:
        abstract = True
        fields = ("user", "recipe")

    def to_representation(self, instance):
        serializer = Short_Recipe_Serializer(
            instance.recipe,
            context=self.context
        )
        return serializer.data

    def validate(self, data, related_name):
        user = data.get("user")
        recipe = data.get("recipe")

        if getattr(user, related_name).filter(recipe__id=recipe.id).exists():
            raise serializers.ValidationError(
                "Комбинация существует"
            )

        return data

class Favorite_Serializer(Recipe_Collection_Serializer):
    class Meta:
        model = User_Favorite
        fields = ("user", "recipe")

class Cart_Serializer(Recipe_Collection_Serializer):
    class Meta:
        model = User_Cart
        fields = ("user", "recipe") 