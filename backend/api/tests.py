from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

class RecipeAPITests(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_recipe(self):
        """Тест создания рецепта"""
        url = reverse('api:recipe-list')
        data = {
            'name': 'Тестовый рецепт',
            'text': 'Описание рецепта',
            'cooking_time': 30,
            'image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==',
            'ingredients': [
                {'name': 'Ингредиент 1', 'amount': 100, 'measurement_unit': 'г'},
                {'name': 'Ингредиент 2', 'amount': 200, 'measurement_unit': 'мл'}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])

    def test_get_recipes(self):
        """Тест получения списка рецептов"""
        url = reverse('api:recipe-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_recipe_detail(self):
        """Тест получения деталей рецепта"""
        # Сначала создаем рецепт
        url = reverse('api:recipe-list')
        data = {
            'name': 'Тестовый рецепт',
            'text': 'Описание рецепта',
            'cooking_time': 30,
            'image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==',
            'ingredients': [
                {'name': 'Ингредиент 1', 'amount': 100, 'measurement_unit': 'г'}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipe_id = response.data['id']

        # Теперь получаем детали рецепта
        url = reverse('api:recipe-detail', kwargs={'pk': recipe_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])

class UserAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_registration(self):
        """Тест регистрации пользователя"""
        url = reverse('api:user-list')
        data = {
            'username': 'newuser123',
            'email': 'new@example.com',
            'password': 'newpass123',
            'first_name': 'Новый',
            'last_name': 'Пользователь'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])

    def test_user_login(self):
        """Тест входа пользователя"""
        url = reverse('api:token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
