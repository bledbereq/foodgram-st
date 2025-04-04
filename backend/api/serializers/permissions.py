from rest_framework import permissions

class Ownership_Permission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Проверяем, является ли метод безопасным или пользователь авторизован
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user and request.user.is_authenticated)
        )

    def has_object_permission(self, request, view, obj):
        # Разрешаем доступ через безопасные методы или если пользователь — владелец объекта
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user and obj.author == request.user)
        )