from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from accounts.serializers import ManagementProfileSerializer, StudentProfileSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

# student profile section
class StudentUpdateProfile(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        user = request.user
        users_data = StudentProfile.objects.get(user= user)
        user_serializer = StudentProfileSerializer(users_data, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request):
        '''
        abc
        '''
        user = request.user
        # objects
        users_data = StudentProfile.objects.get(user= user)
        user_email_obj = users_data.user
        user_serializer = UserSerializer(user_email_obj)
        user_profile_serializer = StudentProfileSerializer(users_data)
        return Response({'email':user_serializer.data,"profile":user_profile_serializer.data},status=status.HTTP_200_OK)

class ManagementUpdateProfile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        # objects
        users_data = ManagementProfile.objects.get(user= user)
        user_email_obj = users_data.user
        user_serializer = UserSerializer(user_email_obj)
        user_profile_serializer = ManagementProfileSerializer(users_data)
        return Response({'email':user_serializer.data,"profile":user_profile_serializer.data},status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        users_data = ManagementProfile.objects.get(user= user)
        user_serializer = ManagementProfileSerializer(users_data, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


