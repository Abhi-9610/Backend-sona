from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager
import uuid
from django.utils import timezone

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CustomUser(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    id_number=models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    profile = models.ImageField(upload_to="uploads/images/profile/")
    role = models.IntegerField()  
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_active = models.BooleanField(default=True)
    owner_id=models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile']

    objects = CustomUserManager()

class UserProfile(TimeStampedModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='subuser')
    
    password = models.CharField(max_length=128, blank=True, null=True)

class ProductsModels(models.Model):
       name=models.CharField(max_length=50)
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)
       desc=models.CharField(max_length=255)
       image=models.ImageField(upload_to="uploads/images/products/")
       Products_id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
       owner_id=models.CharField(max_length=255)


class LoactionModel(models.Model):
     owner_id=models.CharField(max_length=100)
     name=models.CharField(max_length=50)
     unique_id=models.UUIDField(default=uuid.uuid4,unique=True)
     ip=models.CharField(max_length=20)
     port=models.CharField(max_length=6)


class ReviewModel(models.Model):
     rating=models.CharField(max_length=1)
     comment=models.CharField(max_length=100,null=True,blank=True)
     owner_id=models.CharField(max_length=100)