from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from api.serializers.permissions import Ownership_Permission
from recipe.models import Recipe
from django.core.files.uploadedfile import SimpleUploadedFile

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

class TestOwnershipPermission(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()  # Добавляем APIClient для работы с файлами
        
        # Создаем двух уникальных пользователей
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@example.com",  # Уникальный email
            password="password"
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",  # Уникальный email
            password="password"
        )
        
        # Создаем рецепт, автором которого является user1
        self.image = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"file_content",
            content_type="image/jpeg"
        )
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            author=self.user1,
            image=self.image,  # Обязательное поле
            text="Описание рецепта",
            cooking_time=30
        )

    def test_has_object_permission_owner(self):
        """
        Тест: Владелец объекта должен иметь доступ.
        """
        request = self.factory.get("/")  # Используем безопасный метод GET
        request.user = self.user1  # Владелец рецепта
        view = APIView()
        permission = Ownership_Permission()

        has_permission = permission.has_object_permission(request, view, self.recipe)
        self.assertTrue(has_permission, "Владелец не имеет доступа к своему объекту!")

    def test_has_object_permission_not_owner(self):
        """
        Тест: Не владелец объекта может просматривать объект через безопасные методы.
        """
        request = self.factory.get("/")  # Используем безопасный метод GET
        request.user = self.user2  # Другой пользователь (не владелец)
        view = APIView()
        permission = Ownership_Permission()

        has_permission = permission.has_object_permission(request, view, self.recipe)
        self.assertTrue(has_permission, "Не владелец не может просматривать объект через безопасные методы!")

    def test_has_permission_safe_methods(self):
        """
        Тест: Незарегистрированный пользователь может использовать безопасные методы.
        """
        request = self.factory.get("/")  # Используем безопасный метод GET
        request.user = None  # Неавторизованный пользователь
        view = APIView()
        permission = Ownership_Permission()

        has_permission = permission.has_permission(request, view)
        self.assertTrue(has_permission, "Безопасные методы недоступны для незарегистрированных пользователей!")

    def test_has_permission_unauthenticated(self):
        """
        Тест: Незарегистрированный пользователь не может использовать небезопасные методы.
        """
        request = self.factory.post("/")  # Используем небезопасный метод POST
        request.user = None  # Неавторизованный пользователь
        view = APIView()
        permission = Ownership_Permission()

        has_permission = permission.has_permission(request, view)
        self.assertFalse(has_permission, "Незарегистрированные пользователи могут использовать небезопасные методы!")

    def test_has_permission_authenticated(self):
        """
        Тест: Авторизованный пользователь может использовать любые методы.
        """
        request = self.factory.post("/")  # Используем небезопасный метод POST
        request.user = self.user1  # Авторизованный пользователь
        view = APIView()
        permission = Ownership_Permission()

        has_permission = permission.has_permission(request, view)
        self.assertTrue(has_permission, "Авторизованные пользователи не могут использовать небезопасные методы!")
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()  # Добавляем APIClient для работы с файлами
        
        # Создаем двух уникальных пользователей
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@example.com",  # Уникальный email
            password="password"
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",  # Уникальный email
            password="password"
        )
        
        # Создаем рецепт, автором которого является user1
        self.image = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"file_content",
            content_type="image/jpeg"
        )
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            author=self.user1,
            image=self.image,  # Обязательное поле
            text="Описание рецепта",
            cooking_time=30
        )

    def test_has_object_permission_owner(self):
        """
        Тест: Владелец объекта должен иметь доступ.
        """
        request = self.factory.get("/")  # Используем безопасный метод GET
        request.user = self.user1  # Владелец рецепта
        view = APIView()
        permission = Ownership_Permission()

        has_permission = permission.has_object_permission(request, view, self.recipe)
        self.assertTrue(has_permission, "Владелец не имеет доступа к своему объекту!")

    def test_has_object_permission_not_owner(self):
        """
        Тест: Не владелец объекта может просматривать объект через безопасные методы.
        """
        request = self.factory.get("/")  # Используем безопасный метод GET
        request.user = self.user2  # Другой пользователь (не владелец)
        view = APIView()
        permission = Ownership_Permission()

        has_permission = permission.has_object_permission(request, view, self.recipe)
        self.assertTrue(has_permission, "Не владелец не может просматривать объект через безопасные методы!")

    def test_has_permission_safe_methods(self):
        """
        Тест: Незарегистрированный пользователь может использовать безопасные методы.
        """
        request = self.factory.get("/")  # Используем безопасный метод GET
        request.user = None  # Неавторизованный пользователь
        view = APIView()
        permission = Ownership_Permission()

        has_permission = permission.has_permission(request, view)
        self.assertTrue(has_permission, "Безопасные методы недоступны для незарегистрированных пользователей!")

    def test_has_permission_unauthenticated(self):
        """
        Тест: Незарегистрированный пользователь не может использовать небезопасные методы.
        """
        request = self.factory.post("/")  # Используем небезопасный метод POST
        request.user = None  # Неавторизованный пользователь
        view = APIView()
        permission = Ownership_Permission()

        has_permission = permission.has_permission(request, view)
        self.assertFalse(has_permission, "Незарегистрированные пользователи могут использовать небезопасные методы!")

    def test_has_permission_authenticated(self):
        """
        Тест: Авторизованный пользователь может использовать любые методы.
        """
        request = self.factory.post("/")  # Используем небезопасный метод POST
        request.user = self.user1  # Авторизованный пользователь
        view = APIView()
        permission = Ownership_Permission()

        has_permission = permission.has_permission(request, view)
        self.assertTrue(has_permission, "Авторизованные пользователи не могут использовать небезопасные методы!")
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()  # Добавляем APIClient для работы с файлами
        
        # Создаем двух уникальных пользователей
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@example.com",  # Уникальный email
            password="password"
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",  # Уникальный email
            password="password"
        )
        
        # Создаем рецепт, автором которого является user1
        self.image = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"file_content",
            content_type="image/jpeg"
        )
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            author=self.user1,
            image=self.image,  # Обязательное поле
            text="Описание рецепта",
            cooking_time=30
        )

    def test_has_object_permission_owner(self):
        """
        Тест: Владелец объекта должен иметь доступ.
        """
        request = self.factory.get("/")  # Используем безопасный метод GET
        request.user = self.user1  # Владелец рецепта
        view = APIView()
        permission = Ownership_Permission()

        has_permission = permission.has_object_permission(request, view, self.recipe)
        self.assertTrue(has_permission, "Владелец не имеет доступа к своему объекту!")

    def test_has_object_permission_not_owner(self):
        """
        Тест: Не владелец объекта может просматривать объект через безопасные методы.
        """
        request = self.factory.get("/")  # Используем безопасный метод GET
        request.user = self.user2  # Другой пользователь (не владелец)
        view = APIView()
        permission = Ownership_Permission()

        has_permission = permission.has_object_permission(request, view, self.recipe)
        self.assertTrue(has_permission, "Не владелец не может просматривать объект через безопасные методы!")

    def test_has_permission_safe_methods(self):
        """
        Тест: Незарегистрированный пользователь может использовать безопасные методы.
        """
        request = self.factory.get("/")  # Используем безопасный метод GET
        request.user = None  # Неавторизованный пользователь
        view = APIView()
        permission = Ownership_Permission()

        has_permission = permission.has_permission(request, view)
        self.assertTrue(has_permission, "Безопасные методы недоступны для незарегистрированных пользователей!")

    def test_has_permission_unauthenticated(self):
        """
        Тест: Незарегистрированный пользователь не может использовать небезопасные методы.
        """
        request = self.factory.post("/")  # Используем небезопасный метод POST
        request.user = None  # Неавторизованный пользователь
        view = APIView()
        permission = Ownership_Permission()

        has_permission = permission.has_permission(request, view)
        self.assertFalse(has_permission, "Незарегистрированные пользователи могут использовать небезопасные методы!")

    def test_has_permission_authenticated(self):
        """
        Тест: Авторизованный пользователь может использовать любые методы.
        """
        request = self.factory.post("/")  # Используем небезопасный метод POST
        request.user = self.user1  # Авторизованный пользователь
        view = APIView()
        permission = Ownership_Permission()

        has_permission = permission.has_permission(request, view)
        self.assertTrue(has_permission, "Авторизованные пользователи не могут использовать небезопасные методы!")