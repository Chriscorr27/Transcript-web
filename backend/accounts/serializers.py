from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import ManagementProfile, StudentProfile

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id','email','is_management','password')

class ManagementProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagementProfile
        fields = ('user', 'staff_id', 'name', 'contact_no', 'accepted', 'rejected')

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ('user', 'sap_id', 'name', 'contact_no', 'department', 'admission_year')
    