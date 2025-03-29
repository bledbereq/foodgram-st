from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from .recipe import Short_Recipe_Serializer

User = get_user_model()

class Author_Serializer(serializers.ModelSerializer):
    avatar = Base64ImageField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "avatar", "is_subscribed")

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.subscribers.filter(id=request.user.id).exists()

class UserSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'avatar')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class Avatar_Serializer(serializers.ModelSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ("avatar",)

class Subscriber_Serializer(Author_Serializer):
    recipes = serializers.SerializerMethodField(method_name="get_recipes")
    recipes_count = serializers.IntegerField(source="recipes.count")

    class Meta:
        model = User
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