from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import ManagementProfile, StudentProfile
from .serializers import ManagementProfileSerializer, StudentProfileSerializer
from djoser.views import UserViewSet
from djoser import signals
from djoser.compat import get_user_email
from djoser.conf import settings as DjoserSettings

# swagger
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
       
# Create your views here.
class UserInfoApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        data = {
            'email': user.email,
            'is_management':user.is_management,
            'profile_created':user.profileCreated
        }
        return Response(data)

class UserViewSet(UserViewSet):
    # @swagger_auto_schema(method='post', request_body=openapi.Schema(
    # type=openapi.TYPE_OBJECT, 
    # properties={
    #     'x': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    #     'y': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    # }))
    def perform_create(self, serializer):
        user = serializer.save()
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )
        if self.request.data.get('profile', False):
            self.request.data['profile']['user'] = user.id
        if self.request.data.get('is_management', False):
            profile = ManagementProfileSerializer(data = self.request.data.get('profile', None))
        else:
            profile = StudentProfileSerializer(data = self.request.data.get('profile', None))
        if not profile.is_valid():
            user.delete()
            raise ValidationError(profile.errors)
        profile.save()
        # Calling super().perform_create(serializer) saves serializer again and messes up password
        
        # Send activation email - 
        context = {"user": user}
        to = [get_user_email(user)]
        if DjoserSettings.SEND_ACTIVATION_EMAIL:
            DjoserSettings.EMAIL.activation(self.request, context).send(to)
        elif DjoserSettings.SEND_CONFIRMATION_EMAIL:
            DjoserSettings.EMAIL.confirmation(self.request, context).send(to)