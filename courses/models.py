from django.db import models
import uuid

from users.models import User

# Create your models here.
class Course(models.Model):
  uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=255, unique=True)
  demo_time = models.DateField()
  created_at = models.DateField()
  link_repo = models.CharField(max_length=255)

  instructor = models.OneToOneField(User, on_delete=models.CASCADE, related_name='course', null=True)
  students = models.ManyToManyField(User, related_name='courses')