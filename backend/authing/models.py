from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
import settings_constants as user_constants


class User(AbstractUser):
    """
    Пользовательская модель пользователя с расширенными полями.
    """
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
    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=user_.USER_CHAR_LEN,
        validators=[
            RegexValidator(regex=user_.USER_REG)
        ],
        unique=True,
        help_text="Уникальное имя пользователя (только буквы, цифры и символы подчеркивания)."
    )
     email = models.EmailField(
        verbose_name="Email",
        max_length=user_.USER_EMAIL_LEN,
        unique=True,
        help_text="Уникальный адрес электронной почты пользователя."
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации",
        help_text="Дата и время регистрации пользователя."
    )
    profile_picture = models.ImageField(
        verbose_name="Фото профиля",
        upload_to="profile_pictures/",
        blank=True,
        null=True,
        help_text="Изображение профиля пользователя (необязательно)."
    )
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("-date_joined",)

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """
    Модель подписок между пользователями.
    """

    target_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscribers",
        verbose_name="Целевой пользователь",
        help_text="Пользователь, на которого подписываются."
    )

    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Подписчик",
        help_text="Пользователь, который подписывается."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время создания подписки."
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=("subscriber", "target_user"),
                name="unique_subscription"
            )
        ]
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.subscriber} подписан на {self.target_user}"