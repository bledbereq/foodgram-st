from djoser.serializers import UserSerializer as DjoserUserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from django.contrib.auth import get_user_model

from ..models import Subscription, User


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(DjoserUserSerializer):
    """Сериалайзер для получения пользователей с дополнительными полями"""

    is_subscribed = serializers.SerializerMethodField()
    avatar = Base64ImageField(required=False)

    class Meta(DjoserUserSerializer.Meta):
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar'
        )
        read_only_fields = ('id', 'username', 'email', 'first_name', 'last_name')

    def get_is_subscribed(self, user):
        request_user = self.context['request'].user
        if not request_user.is_authenticated:
            return False
        return Subscription.objects.filter(
            author=user.id,
            user=request_user.id
        ).exists()


class SubscribedUserSerializer(UserSerializer):
    """Сериалайзер для получения информации об авторах,
    на которых подписан текущий пользователь"""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(
        source='author.recipes.count'
    )

    class Meta(UserSerializer.Meta):
        fields = (
            *UserSerializer.Meta.fields,
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, author):
        from .recipes import ShortRecipeSerializer
        return ShortRecipeSerializer(
            author.recipes.all()[:int(self.context.get('request').GET.get(
                'recipes_limit',
                10**10
            ))],
            many=True
        ).data


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для ответа при создании подписки"""
    user = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    class Meta:
        model = Subscription
        fields = ('user', 'author') 