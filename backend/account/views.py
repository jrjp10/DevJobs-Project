from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from  rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .serializers import UserRegistrationSerializer, LoginSerializer, CompanyProfileSerializer, CandidateProfileSerializer
from .models  import CompanyProfile, CandidateProfile

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


class CompanyProfileCreateView(generics.CreateAPIView):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CandidateProfileCreateView(generics.CreateAPIView):
    queryset = CandidateProfile.objects.all()
    serializer_class = CandidateProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CompanyProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanyProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CompanyProfile.objects.filter(user=self.request.user)
    
    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update this profile.")

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this profile.")

class CandidateProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CandidateProfileSerializer
    authentication_classes  = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CandidateProfile.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update this profile.")
    
    def  perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied(("You do not have permission to update this profile."))
