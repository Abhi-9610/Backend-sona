# face_recognition_app/models.py
from django.db import models

class RegisteredFace(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    encoding = models.JSONField()
    image_path = models.CharField(max_length=255)
    encodings_file_path = models.CharField(max_length=255)
