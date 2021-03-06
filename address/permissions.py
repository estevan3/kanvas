from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
  def has_permission(self, request, view):
    if request.method == "GET":
      return bool(request.user and request.user.is_authenticated and request.user.is_staff)

    return True