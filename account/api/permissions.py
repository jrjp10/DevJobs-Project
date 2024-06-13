from rest_framework.permissions import BasePermission
from ..models import User

class IsCompanyUser(BasePermission):
    
    """
    Custom permission to only allow company users to access the view.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == User.COMPANY
        else:
            # Allow  Get request for listing retrieving public content
            return request.method in ['GET'] and view.action in  ['list', 'retrieve']


class IsCandidateUser(BasePermission):
    """
    Custom permission to only allow candidate users to access the view.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == User.CANDIDATE
        else:
             # Allow  Get request for listing retrieving public content
            return request.method in ['GET'] and view.action in  ['list', 'retrieve']

class IsAdminUser(BasePermission):
    """
    Custom permission to only allow Admin to access the view.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff
    