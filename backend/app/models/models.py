from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
import settings_constants as user_constants

class User(AbstractUser):
    """
    Пользовательская модель пользователя с расширенными полями.
    """

    email = models.EmailField(
        verbose_name="Email",
        max_length=user_.USER_EMAIL_LEN,
        unique=True,
        help_text="Уникальный адрес электронной почты пользователя."
    )

    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=user_.USER_CHAR_LEN,
        validators=[
            RegexValidator(regex=user_.USER_REG)
        ],
        unique=True,
        help_text="Уникальное имя пользователя (только буквы, цифры и символы подчеркивания)."
    )

    first_name = models.CharField(
        verbose_name="Имя",
        max_length=user_.USER_CHAR_LEN,
        help_text="Имя пользователя."
    )

    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=user_.USER_CHAR_LEN,
        help_text="Фамилия пользователя."
    )

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

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

class Subscription(models.Model):
    """Модель подписок"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authors',
        verbose_name='Автор рецептов'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
