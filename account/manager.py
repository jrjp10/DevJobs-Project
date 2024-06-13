from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    """
    Custom User Model where the mail adress is the unique identifier
    and has an is_admin feild to allow access to the admin app
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email feild must be set')
        
        if not password or len(password) < 6:
            raise ValueError('Password must ve at least 6 characters long')
        
        email = self.normalize_email(email)
        user  = self.model(email=email, **extra_fields)
        user.set_password(password)   # Hash the password before saving it in the database
        user.save(using=self._db)     # Using the correct database alias to ensure
        return user                   # that this is the one where the new user will be created
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get( 'role' ) != 'admin':
            raise ValueError("Superuser must have role of Global Admin")
        
        return self.create_user(email, password, **extra_fields)