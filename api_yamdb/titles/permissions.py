from rest_framework import permissions

# Возможно понадобится сделал на будущее
# class Admin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_admin and request.user.is_authenticated


class AdminOrReadOnly(permissions.BasePermission):
    """Проверка - является ли пользователь администратором."""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_admin and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_admin and request.user.is_authenticated
        )

# Возможно понадобится сделал на будущее
# class AuthorOrModerOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return (request.method in permissions.SAFE_METHODS
#                 or obj.author == request.user
#                 or (request.user.is_authenticated
#                     and request.user.is_moderator_or_admin)
#                 )
