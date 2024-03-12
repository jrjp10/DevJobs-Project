from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from  rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, LoginSerializer


# Generate Token Manually
def get_token_for_users(user):
    try:
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    except Exception as e:
        # Log the error for investigation
        print(f"Token generation failed for user {user.email}: {e}")
        # Return None or an empty dictionary indicating failure
        return None

# Create your views here.
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_token_for_users(user)
            response_data = {
                'message': 'User Registraion Successful.',
                'user': UserRegistrationSerializer(user).data,
                'token': token
            }
            return Response(response_data,status=status.HTTP_201_CREATED)
        return  Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token = get_token_for_users(user)
            response_data = {
                'message': 'User login Successfully.',
                'user': LoginSerializer(user).data,
                'token': token
            }
            return Response(response_data, status=status.HTTP_200_OK)             
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)