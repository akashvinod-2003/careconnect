from rest_framework import serializers
from .models import ServiceRequest

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = '__all__'
        read_only_fields = ['family_user', 'assigned_staff', 'status', 'created_at']