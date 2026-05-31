from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)    

class UserAccount(AbstractUser):
    
    objects= CustomUserManager() # type: ignore
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    
    national_code = models.CharField(max_length=10, unique=True, blank=True, null=True, verbose_name='National code')
    email = models.EmailField(unique=True)
    birthday = models.DateField(null = True, blank = True)
    phone = models.CharField(max_length = 20, blank = True)
    city = models.CharField(max_length=25, blank=True, verbose_name='City')
    address = models.CharField(max_length = 250, blank = True)
    postal_code = models.CharField(max_length=10, blank = True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name='Gender')
    emergency_contact = models.CharField(max_length=11, blank=True, verbose_name='Emergency contact number')
    bio = models.TextField(blank=True, verbose_name='Biography/About me')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
