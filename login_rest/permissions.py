from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.permissions import BasePermission

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening



class AuthHROnlyRole(BasePermission):
    """
    Allows access only to Authenticated HR users.
    """
    @staticmethod
    def check_role(request, headers): 
        if 'HR' in request.session['roles']:
            return True
    	return False


    def has_permission(self, request, view):
        return self.check_role(request, request.META)


class AuthHODOnlyRole(BasePermission):
    """
    Allows access only to Authenticated HOD users.
    """
    @staticmethod
    def check_role(request, headers): 
        if 'HOD' in request.session['roles']:
            return True
        return False


    def has_permission(self, request, view):
        return self.check_role(request, request.META)


class AuthEmployeeOnlyRole(BasePermission):
    """
    Allows access only to Authenticated EMPLOYEE users.
    """
    @staticmethod
    def check_role(request, headers): 
        if 'EMPLOYEE' in request.session['roles']:
            return True
        return False


    def has_permission(self, request, view):
        return self.check_role(request, request.META)
