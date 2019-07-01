from rest_framework import permissions
from .models import Apikeys

class ApiPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        api_key = request.query_params.get("apikey", False)
        return Apikeys.objects.filter(api_key=api_key).exists()
