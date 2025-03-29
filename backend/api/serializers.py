from rest_framework import serializers
from recipe.models import Ingredient, Ingredient_In_Recipe
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField

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