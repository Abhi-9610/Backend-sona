from rest_framework import serializers
from .models import *
from drf_extra_fields.fields import Base64ImageField

class robotSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)
    
    
    class Meta:
        model=robotModel
        fields="__all__"

class goalSerializer(serializers.ModelSerializer):
    class Meta:
        model=goalsModel
        fields="__all__"
    
    

