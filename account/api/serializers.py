from rest_framework  import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from account.models import User
from .utils import generate_token
from ..models import CompanyProfile, CandidateProfile

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):

    """
    Serializer for user registration.

    Handles the serialization and deserialization of User objects during the registration process.
    Automatically hashes the password before saving.
    """

    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('uuid','email', 'phone_number', 'role', 'password', 'created_at', 'updated_at', 'token')
        extra_kwargs = {
            'password': {'write_only': True},
            'uuid':{'read_only':True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def get_token(self, obj):
        token = generate_token.make_token(obj)
        return str(token)
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)
    

class LoginSerializer(serializers.Serializer):

    """
    Serializer for user login.

    Handles the serialization and deserialization of User objects during the login process.
    Authenticates users based on provided email and password.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        """
        Validates the login credentials and authenticates the user.
        """

        email = attrs.get('email')
        password = attrs.get('password')

        # check if email and pasword are provided
        if email and password:
            # Authenticate user with provided credentials
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                return user
            else:
                raise serializers.ValidationError("Incorrect email or password.")
        else:
            raise serializers.ValidationError("Both email and password are required.")



class CompanyProfileSerializer(serializers.ModelSerializer):

    """
    Serializer for company profiles.

    Handles the serialization and deserialization of CompanyProfile objects.
    Ensures that only users with the 'company' role can create company profiles.
    """
     
    class Meta:
        model = CompanyProfile
        fields = ('company_name','industry', 'location', 'website', 'description', 'company_image')

    def validate(self, attrs):

        """
        Validates that the user creating the profile has the 'company' role.
        """

        user = self.context['request'].user

        if user.role != User.COMPANY:
            raise serializers.ValidationError("Only users with the role 'company' are allowed to create company profiles.")
        return attrs
        
    def create(self, validated_data, **kwargs):

        """
        Creates a new company profile for the authenticated user.
        """
         
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data, **kwargs)
    

class PublicCompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'industry', 'location', 'website', 'description', 'company_image']



    
class CandidateProfileSerializer(serializers.ModelSerializer):

    """
    Serializer for candidate profiles.

    Handles the serialization and deserialization of CandidateProfile objects.
    Ensures that only users with the 'candidate' role can create candidate profiles.
    """    

    class Meta:
        model = CandidateProfile
        fields = ('name', 'birthday', 'location', 'skills', 'experience', 'education',  'resume', 'candidate_image')
        extra_kwargs = {
            'resume': {'default': ''}  # Providing a default value for the resume field
        }
    
    def validate(self, attrs):

        """
        Validates that the user creating the profile has the 'candidate' role.
        """

        user = self.context['request'].user

        if  user.role != User.CANDIDATE:
            raise serializers.ValidationError("Only users with the role 'candidate' are allowed to create candidate profiles.")
        return attrs
    
    def  create(self, validated_data, **kwargs):

        """
        Creates a new candidate profile for the authenticated user.
        """
         
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data, **kwargs)