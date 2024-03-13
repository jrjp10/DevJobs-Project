from .manager import UserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.hashers import make_password

# Create your models here.
class User(AbstractUser, PermissionsMixin):
    COMPANY = 'company'
    CANDIDATE = 'candidate'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (COMPANY, 'Company'),
        (CANDIDATE, 'Candidate'),
        (ADMIN, 'Admin'),
    ]

    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=14)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CANDIDATE)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)          # Administrator user
    is_staff = models.BooleanField(default=False)

    # Extra fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    # Set the fields from AbstractUser to None to exclude them from being saved
    first_name = None
    last_name = None
    

    def __str__(self):
        return self.username

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='user', related_name='company_profile')
    company_name = models.CharField(max_length=255, verbose_name='company_name')
    industry = models.CharField(max_length=100, verbose_name='industry')
    location = models.CharField(max_length=255, verbose_name='location')
    website = models.URLField(max_length=200, verbose_name='website', blank=True, null=True)
    description = models.TextField(verbose_name='description', blank=True, null=True)

    class Meta:
        verbose_name = 'company_profile'
        verbose_name_plural = 'company_profiles'
        db_table = 'company_profile'

    def __str__(self):
        return self.company_name

class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='user', related_name='candidate_profile')
    birthday = models.DateField(verbose_name='birth date', blank=True, null=True)
    location = models.CharField(max_length=255, verbose_name='location')
    skills = models.CharField(max_length=255, verbose_name='skills', blank=True, null=True)
    experience = models.CharField(max_length=100, verbose_name='experience', blank=True, null=True)
    education = models.CharField(max_length=255, verbose_name='education', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', verbose_name='resume', blank=True, null=True)

    class Meta:
        verbose_name = 'candidate_profile'
        verbose_name_plural = 'candidate_profiles'
        db_table = 'candidate_profile'

    def __str__(self):
        return f"{self.user.username}'s Profile"

    

