from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Разрешение, позволяющее только администраторам выполнять действия.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее только администраторам выполнять
    небезопасные действия. Остальные пользователи могут только читать.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее админам, модераторам и авторам контента
    выполнять небезопасные действия.
    Остальные пользователи могут только читать.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        return (
            obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
