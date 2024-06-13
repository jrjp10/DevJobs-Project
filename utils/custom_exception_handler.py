from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # Call the default exception handler first
    # to get the standerd error response
    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__

    print(exception_class)

    if exception_class == "AuthenticationFailed":
        response.data = {
            "error": "Invalid Email or Password.Try again",
            
        }
    
    if exception_class == "NotAuthenticated":
        response.data = {
            "error": "Login first to access this resourse"
        }
    
    if exception_class == "InvalidToken":
        response.data = {
            "error": "Your authentication token is expired.Please login again"
        }
    
    if exception_class == "PermissionDenied":
        response.data = {
            "error": "You do not have permission to perform this action.",
            "error_code": "authentication_failed"
        }
    

    return response