from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

# Create your models here.
class CustomUserManeger(BaseUserManager):
  def _create_user(self, email, password, first_name, last_name, is_staff, is_superuser, is_admin=False, **extra_fields):
    now = timezone.now()

    if not email:
      raise ValueError('The given email must be set')
    
    email = self.normalize_email(email)

    user = self.model(email=email, first_name=first_name, last_name=last_name, is_staff=is_staff, is_admin=is_admin, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)

    user.set_password(password)

    user.save(using=self._db)

    return user
  
  def create_user(self, email, password, first_name, last_name, is_admin=False, **extra_fields):
    return self._create_user(email,password,first_name, last_name, False, is_admin, is_admin)
  
  def create_superuser(self, email, password, first_name, last_name, is_admin=True, **extra_fields):
    return self._create_user(email, password, first_name, last_name, True, is_admin, is_admin)


class User(AbstractUser):
  uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  is_admin = models.BooleanField(default=False)
  email = models.EmailField(max_length=255, unique=True)
  password = models.CharField(max_length=255)
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  username = models.CharField(unique=False, null=True, max_length=255)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name']

  objects = CustomUserManeger()