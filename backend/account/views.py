from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from  rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from .serializers import UserRegistrationSerializer, LoginSerializer, CompanyProfileSerializer, CandidateProfileSerializer, UserChangePasswordSerializer
from .models  import User, CompanyProfile, CandidateProfile


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

# To create Company Profile
class CompanyProfileCreateView(generics.CreateAPIView):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != User.COMPANY:
            return Response({"error": "Only users with the role 'company' are allowed to create company profiles."}, status=status.HTTP_403_FORBIDDEN)
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            return Response({"error": "A company profile already exists for this user."}, status=status.HTTP_400_BAD_REQUEST)


# To create Candidate Profile
class CandidateProfileCreateView(generics.CreateAPIView):
    queryset = CandidateProfile.objects.all()
    serializer_class = CandidateProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != User.CANDIDATE:
            return Response({"error": "Only users with the role 'Candidate' are allowed to create Candidate profiles."}, status=status.HTTP_403_FORBIDDEN)
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            return Response({"error": "A candidate profile already exists for this user."}, status=status.HTTP_400_BAD_REQUEST)
        
# TO list all the Candidate
class CandidateProfileListView(generics.ListAPIView):
    queryset = CandidateProfile.objects.all()
    serializer_class = CandidateProfileSerializer


# TO list all the Company
class ComapanyProfileListView(generics.ListAPIView):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer



# For CRUD Operation of Company Profile
class CompanyProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanyProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes  = [JWTAuthentication]


    def get_queryset(self):
        return CompanyProfile.objects.filter(user=self.request.user)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        if self.request.user.role != User.COMPANY or obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to perform this action.")
        return obj
    
    def perform_update(self, serializer):
        try:
            instance = serializer.save()
            return Response({"message": "Company profile updated successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def perform_destroy(self, instance):
        try:
            instance.delete()
            return Response({"message": "Company profile deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Exception  as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    


# For CRUD Operation of Candidate Profile
class CandidateProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CandidateProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes  = [JWTAuthentication]


    def get_queryset(self):
        return CandidateProfile.objects.filter(user=self.request.user)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        if self.request.user.role != User.CANDIDATE or obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to perform this action.")
        return obj
    
    def perform_update(self, serializer):
        try:
            instance = serializer.save()
            return Response({"message": "Candidate profile updated successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def perform_destroy(self, instance):
        try:
            instance.delete()
            return Response({"message": "Candidate profile deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserChangePasswordUpdateView(generics.UpdateAPIView):
    serializer_class = UserChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Retrive the current User
        user = self.request.user
        # Get old and new  password from request data
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        # Check if old password is correct
        if not user.check_password(old_password):
            return Response({'error':"Old password doesn't match"})

        # Change  Password
        try:
            user.set_password(new_password)
            user.save()
            return Response({"Message": "Password Changed Successfully"})
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)





















# class SendPasswordResetEmailView(generics.GenericAPIView):
#     serializer_class = SendPasswordResetEmailSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     def post(self, request, format=None):
#         serializer = SendPasswordResetEmailSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


