from django.db import models
from .manager import UserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
import uuid

# Create your models here.


class User(AbstractUser, PermissionsMixin):
    """
    Custom user model that extends Django's AbstractUser and PermissionsMixin.
    This model uses email as the username and includes additional fields such as phone number and role.
    """
    COMPANY = 'company'
    CANDIDATE = 'candidate'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (COMPANY, 'Company'),
        (CANDIDATE, 'Candidate'),
        (ADMIN, 'Admin'),
    ]
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='Email', max_length=255, unique=True)
    phone_number = models.CharField(max_length=14)
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default=CANDIDATE)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # Administrator user
    is_staff = models.BooleanField(default=False)

    # Extra fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # Set the fields from AbstractUser to None to exclude them from being saved
    first_name = None
    last_name = None
    username = None

    def __str__(self):
        return self.email

    @property
    def id(self):
        return self.uuid


class CompanyProfile(models.Model):

    """
    Model to store company profiles linked to the User model.
    Each company profile contains information about the company such as name, industry, location, website, and description.
    """

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='user', related_name='company_profile')
    company_name = models.CharField(
        max_length=255, verbose_name='company_name')
    industry = models.CharField(max_length=100, verbose_name='industry')
    location = models.CharField(max_length=255, verbose_name='location')
    website = models.URLField(
        max_length=200, verbose_name='website', blank=True, null=True)
    description = models.TextField(
        verbose_name='description', blank=True, null=True)
    company_image = models.ImageField(upload_to='company_images', blank=True, null=True)

    class Meta:
        verbose_name = 'company_profile'
        verbose_name_plural = 'company_profiles'
        db_table = 'company_profile'

    def __str__(self):
        return self.company_name

    @property
    def id(self):
        return self.uuid


class CandidateProfile(models.Model):

    """
    Model to store candidate profiles linked to the User model.
    Each candidate profile contains personal information such as name, birthday, location, skills, experience, education, and resume.
    """
    
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='user', related_name='candidate_profile')
    name = models.CharField(verbose_name='name', blank=False, null=False)
    birthday = models.DateField(
        verbose_name='birth date', blank=True, null=True)
    location = models.CharField(max_length=255, verbose_name='location')
    skills = models.CharField(
        max_length=255, verbose_name='skills', blank=True, null=True)
    experience = models.CharField(
        max_length=100, verbose_name='experience', blank=True, null=True)
    education = models.CharField(
        max_length=255, verbose_name='education', blank=True, null=True)
    resume = models.FileField(
        upload_to='resumes/', blank=True)
    candidate_image = models.ImageField(
        upload_to='candidate_images/', blank=True, null=True)

    class Meta:
        verbose_name = 'candidate_profile'
        verbose_name_plural = 'candidate_profiles'
        db_table = 'candidate_profile'

    def __str__(self):
        return f"{self.name}'s Profile"

    @property
    def id(self):
        return self.uuid
