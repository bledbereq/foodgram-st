from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """
    Модель пользователей системы.
    Наследуется от AbstractUser Django для базовой
    функциональности аутентификации.
    Использует email в качестве основного идентификатора пользователя.
    Attributes:
        email (EmailField): Уникальный email пользователя
        username (CharField): Уникальное имя пользователя с валидацией символов
        first_name (CharField): Имя пользователя
        last_name (CharField): Фамилия пользователя
        avatar (ImageField): Аватар пользователя (опционально)
    """

    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Email',
        help_text='Уникальный email пользователя'
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя',
        help_text='Уникальное имя пользователя',
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Username должен содержать только буквы, '
                    'цифры и следующие символы: @ . + -'
        )]
    )

    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя',
        help_text='Имя пользователя'
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия',
        help_text='Фамилия пользователя'
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар',
        help_text='Изображение профиля пользователя'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'password'
    ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('email',)

    def __str__(self):
        return self.email
