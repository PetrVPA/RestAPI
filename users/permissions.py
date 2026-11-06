from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsModerator(permissions.BasePermission):
    """
    Разрешение, проверяющее, является ли пользователь модератором.
    """

    def has_permission(self, request, view):
        # Проверка, что пользователь авторизован
        if not request.user or not request.user.is_authenticated:
            return False

        # Проверка принадлежности к группе 'moderators' (имя группы задайте свое)
        return request.user.groups.filter(name='moderators').exists()


class IsOwner(permissions.BasePermission):
    """
    Разрешение, проверяющее, что пользователь является владельцем объекта.
    """
    def has_object_permission(self, request, view, obj):
        # Если у объекта есть поле owner, проверяем совпадение
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        # Для уроков может понадобиться проверять владельца через курс (если у урока нет своего owner)
        # return obj.course.owner == request.user
        return False

class IsNotModerator(BasePermission):
    def has_permission(self, request, view):
        # Если пользователь авторизован и НЕ входит в группу модераторов
        return request.user.is_authenticated and not request.user.groups.filter(name='moderators').exists()