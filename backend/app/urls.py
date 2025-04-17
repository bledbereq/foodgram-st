from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    RecipeViewSet,
    IngredientViewSet,
)
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')

app_name = 'app'

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')
]
