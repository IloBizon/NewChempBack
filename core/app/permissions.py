from rest_framework import permissions

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_doctor
class IsDoctorOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        # Только авторизованные пользователи
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Доктор может всё
        if request.user.is_doctor:
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user