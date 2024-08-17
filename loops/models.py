# models.py

from django.db import models
import uuid

class loops(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roboid = models.CharField(max_length=100)
    
    time_delay_seconds = models.IntegerField(null=True)
    timestring=models.CharField(max_length=100,null=True)
    admin_id = models.CharField(max_length=100)
    type = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class loopevent(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner_id = models.CharField(max_length=100)
    goalid = models.CharField(max_length=100)
    type = models.CharField(max_length=10)
    
