# face_recognition_app/serializers.py
from rest_framework import serializers
from .models import RegisteredFace

class RegisteredFaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredFace
        fields = ['name','image_path','age']
