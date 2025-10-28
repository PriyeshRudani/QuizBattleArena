from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    Admin is determined by profile role or Django is_staff/is_superuser.
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check if user has admin role or is staff/superuser
        if hasattr(request.user, 'profile'):
            return request.user.profile.is_admin()
        
        return request.user.is_staff or request.user.is_superuser


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read-only access to everyone,
    but write access only to admin users.
    """
    
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for admin users
        if not request.user or not request.user.is_authenticated:
            return False
        
        if hasattr(request.user, 'profile'):
            return request.user.profile.is_admin()
        
        return request.user.is_staff or request.user.is_superuser


class IsUserRole(permissions.BasePermission):
    """
    Custom permission to only allow regular users (not admins) to access.
    Used for quiz-playing endpoints that admins shouldn't access.
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Only allow if user has 'user' role (not admin)
        if hasattr(request.user, 'profile'):
            return request.user.profile.role == 'user'
        
        return not (request.user.is_staff or request.user.is_superuser)
