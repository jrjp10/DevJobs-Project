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

 
    

    