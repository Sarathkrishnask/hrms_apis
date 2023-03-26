from rest_framework import permissions
from django.contrib import auth

class ISEmployeeorAdminOrSuperAdminorEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return str(request.user.roles) in ['SuperAdmin','Admin','Employee']

class ISSuperAdminorEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return str(request.user.roles) in ["SuperAdmin","Employee"]

class ISAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return str(request.user.roles) in ["Admin","SuperAdmin"]

class ISAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return str(request.user.roles) in ["Admin"]

class ISSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return str(request.user.roles) in ["SuperAdmin"]

class ISEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return str(request.user.roles) in ["Employee"]
    
