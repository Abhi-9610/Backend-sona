# serializers.py

from rest_framework import serializers
from .models import loops, loopevent

class loopeventSerializer(serializers.ModelSerializer):
    class Meta:
        model = loopevent
        fields = "__all__"

class loopsSerializer(serializers.ModelSerializer):
    events = loopeventSerializer(many=True, read_only=True)

    class Meta:
        model = loops
        fields = "__all__"


class taskSerializer(serializers.ModelSerializer):

    class Meta:
        model=loops
        fields=['name','timestring','roboid','type','unique_id']
