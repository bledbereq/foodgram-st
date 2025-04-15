from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from auth_user.models import Subscription, User


@admin.register(User)
class UserAdmin(UserAdmin):
    """
    Настройка отображения модели User в административной панели.
    """
    list_display = (
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "profile_picture",
        "date_joined"
    )
    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name"
    )
    list_filter = (
        "is_active",
        "is_staff",
        "date_joined"
    )
    ordering = ("-date_joined",)

    # Переопределение полей для редактирования пользователя
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Персональная информация", {"fields": ("first_name", "last_name", "email", "profile_picture")}),
        ("Права доступа", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

    # Поля для создания нового пользователя
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "first_name", "last_name", "profile_picture"),
        }),
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Настройка отображения модели Subscription в административной панели.
    """
    list_display = (
        "id",
        "subscriber",
        "target_user",
        "created_at"
    )
    search_fields = (
        "subscriber__username",
        "target_user__username",
        "subscriber__email",
        "target_user__email"
    )
    list_filter = (
        "created_at",
    )
    ordering = ("-created_at",)

    def get_queryset(self, request):
        """
        Оптимизация запросов для уменьшения количества обращений к базе данных.
        """
        return super().get_queryset(request).select_related("subscriber", "target_user")