from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from account.models import User
from .models import CompanyProfile, CandidateProfile


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','email', 'phone_number',  'role','password', 'created_at', 'updated_at')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password']=make_password(validated_data.get('password'))
        return super().create(validated_data)
    


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
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
    class Meta:
        model = CompanyProfile
        fields = ('company_name','industry', 'location', 'website', 'description')

    def validate(self, attrs):
        user = self.context['request'].user
        if user.role != User.COMPANY:
            raise serializers.ValidationError("Only users with the role 'company' are allowed to create company profiles.")
        return attrs
        
    def create(self, validated_data, **kwargs):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data, **kwargs)



    
class CandidateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = ('name', 'birthday', 'location', 'skills', 'experience', 'education',  'resume')
    
    def validate(self, attrs):
        user = self.context['request'].user
        if  user.role != User.CANDIDATE:
            raise serializers.ValidationError("Only users with the role 'candidate' are allowed to create candidate profiles.")
        return attrs
    
    def  create(self, validated_data, **kwargs):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data, **kwargs)