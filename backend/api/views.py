from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from recipe.models import Recipe
from .serializers import RecipeSerializer, UserSerializer

User = get_user_model()

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Разрешаем регистрацию без аутентификации
