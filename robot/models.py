from django.db import models
import uuid
from backend.models import CustomUser



# Create your models here.
class robotModel(models.Model):
    name=models.CharField(max_length=20)
    unique_id=models.UUIDField(default=uuid.uuid4,unique=True)
    ip=models.CharField(max_length=20,unique=True)
    port=models.CharField(max_length=20)
    image=models.ImageField(upload_to='uploads/images/robots/')
    created_at=models.DateTimeField(auto_now_add=True)
    owner_id=models.CharField(max_length=100)
    online = models.BooleanField(default=True)
    own = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name


class goalsModel(models.Model):
    unique_id=models.UUIDField(default=uuid.uuid4,unique=True)
    owner_id=models.CharField(max_length=100)
    name=models.CharField(max_length=20)
    message=models.CharField(max_length=100)
    audio=models.FileField(upload_to='uploads/images/profile')
    random=models.CharField(max_length=100,unique=True)
    is_active = models.BooleanField(default=True)
    

