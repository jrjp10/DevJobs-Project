from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed

from .serializers import *
from ..models import *
from .permissions import *
# from backend.utils.custom_exception_handler import *
User = get_user_model()


# Create your views here.


class UserRegistration(APIView):

    """
    API view for user registration.

    Allows users to register by providing necessary information.
    Sends an account activation email upon successful registration.
    """

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate activation Token  for the user and send it to his email id
            token = generate_token.make_token(user)

            uidb64 = urlsafe_base64_encode(force_bytes(user.uuid))
            activation_url = request.build_absolute_uri(
                reverse('account:activate', kwargs={'uidb64': uidb64, 'token': token}))

            # Send Activation mailc
            send_mail(
                subject="Activate Your Account",
                message=f"Please click the following link to activate your account: {activation_url}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            return Response(
                {'message': "User registration success. Check Your Email for Account activation Link.",'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccountView(APIView):

    """
    API view for account activation.

    Activates user account when the user clicks on the activation link sent via email.
    """
     
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(uuid=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': "Account activated successfully."})
        else:
            return Response({'error': "Invalid activation link."}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    """
    API view for user login.

    Allows users to log in by providing their email and password.
    Returns an authentication token upon successful login.
    """

    def post(self, request, *args, **kwargs):

        serializer = LoginSerializer(data=request.data)

        # Validate serializer
        if serializer.is_valid():
            # Get validated user from serializer
            user = serializer.validated_data

            # Generate token for user
            token = get_token_for_users(user)

            # Response data
            response_data = {
                'message': 'User logged in Successfully.',
                'user': LoginSerializer(user).data,
                'token': token
            }
            # Return success response
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed("Incorrect email or password.")
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyProfileCreateView(APIView):

    """
    API view for creating company profiles.

    Allows authenticated users with the 'company' role to create a company profile.
    """

    permission_classes = [IsAuthenticated, IsCompanyUser]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = CompanyProfileSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
                return Response({"message": "Company profile created successfully."}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "A company profile already exists for this user."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CandidateProfileCreateView(APIView):

    """
    API view for creating candidate profiles.

    Allows authenticated users with the 'candidate' role to create a candidate profile.
    """

    permission_classes = [IsAuthenticated, IsCandidateUser]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        if user.role != User.CANDIDATE:
            return Response({"error": "Only users with the role 'candidate' are allowed to create candidate profiles."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = CandidateProfileSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
                return Response({"message": "Candidate profile created successfully."}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "A candidate profile already exists for this user."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#  To perform updata, retrive and delete on companyprofile
class CompanyProfileCRUDView(APIView):

    """
    API view for CRUD operations on company profiles.

    Allows authenticated users with the 'company' role to retrive , update or delete thier company profile
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, uuid):
        obj = get_object_or_404(CompanyProfile, uuid=uuid)
        if self.request.user.role != User.COMPANY or obj.user != self.request.user:
            raise PermissionDenied(
                "You do not have permission to perform this action.")
        return obj

    def get(self, request, uuid):

        """Retrieve a company profile."""

        profile = self.get_object(uuid)
        serializer = CompanyProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, uuid):

        """Update company profile"""

        profile = self.get_object(uuid)
        serializer = CompanyProfileSerializer(
            profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Company profile updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):

        
        """delete a company profile."""

        profile = self.get_object(uuid)
        profile.delete()
        return Response({"message": "Company profile deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


#  To perform updata, retrive and delete on candidateprofile
class CandidateProfileCRUDView(APIView):

    """
    API view for CRUD operations on candidate profiles.

    Allows authenticated users with the 'candidate' role to retrieve, update, or delete their candidate profile.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, uuid):
        obj = get_object_or_404(CandidateProfile, uuid=uuid)
        if self.request.user.role != User.CANDIDATE or obj.user != self.request.user:
            raise PermissionDenied(
                "You do not have permission to perform this action.")
        return obj

    def get(self, request, uuid):

        """Retrieve a candidate profile."""

        profile = self.get_object(uuid)
        serializer = CandidateProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, uuid):

        """Update company profile"""

        profile = self.get_object(uuid)
        serializer = CandidateProfileSerializer(
            profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Candidate profile updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
    
        """delete company profile"""

        profile = self.get_object(uuid)
        profile.delete()
        return Response({"message": "Candidate profile deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



""" 
Admin Dashboard Views 
"""

# To list all the user
class UserListView(APIView):

    """
    API view for listing all users.

    Allows admin users to retrieve a list of all registered users.
    """

    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        # Retrieve all user objects
        users = User.objects.all().order_by('-created_at')

        serializer = UserRegistrationSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        # Retrieve all user objects which is inactive
        inactive_users = User.objects.filter(is_active=False)
        inactive_users.delete()
        return Response({"message": "Inactive users deleted successfully."},
                        status=status.HTTP_204_NO_CONTENT)

class UserDetailView(APIView):
    """
    API view for deleting a specific user by their ID.

    Allows admin users to delete a specific user.
    """
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def delete(self, request,uuid):
        try:
            user = User.objects.get(uuid=uuid)
            user.delete()
            return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

# To list all the candidate user

class CandidateProfileListView(APIView):

    """
    API view for listing all candidate profiles.

    Allows admin users to retrieve a list of all candidate profiles.
    """

    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        profiles = CandidateProfile.objects.all()
        serializer = CandidateProfileSerializer(profiles, many=True)
        return Response(serializer.data)


# To list all the  company user
class CompanyProfileListView(APIView):

    """
    API view for listing all company profiles.

    Allows admin users to retrieve a list of all company profiles.
    """

    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        profiles = CompanyProfile.objects.all()
        serializer = CompanyProfileSerializer(profiles, many=True)
        return Response(serializer.data)
 