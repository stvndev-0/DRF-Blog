from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Se permiten permisos de solo lectura 
        # para cualquier solicitud
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permiso solo a los propietarios
        return obj.user == request.user