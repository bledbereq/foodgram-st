from rest_framework import serializers
from recipe.models import Ingredient, Ingredient_In_Recipe

class Ingredient_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "meas_unit")
        read_only_fields = ("id", "name", "meas_unit")

class Ingredient_Recipe_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient_In_Recipe
        fields = ("id", "name", "meas_unit", "amount")
