from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from .serializer import *
from .models import *
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from django.http.response import Http404
from django.urls import reverse
import jwt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView

# Create your views here.
class Register(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializers
    # renderer_classes = (UserRenderer,)
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
       
        return Response(user_data, status=status.HTTP_201_CREATED)    
class Login(generics.GenericAPIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #user_instance = serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class userData(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializers(self.request.user)
        return Response(serializer.data)

# update the user details
class update_profile(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializers
    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# prefred gender CURD
class PrefredGenderAPIview(APIView):
    permission_classes = [AllowAny]
    def get_object(self, pk):
        try:
            return PrefredGender.objects.get(pk=pk)
        except PrefredGender.DoesNotExist:
            raise Http404
        
    def get(self, request, pk=None, format=None):
            if pk:
                data = self.get_object(pk)
                serializer = PrefredGender(data)
                return Response(serializer.data)

            else:
                data = PrefredGender.objects.all()
                serializer = PrefredGenderSerializers(data, many=True)

                return Response(serializer.data)
            
    def post(self, request, format=None):
        current_user = request.user
        mutable_data = request.data.copy() if request.data else {}
        mutable_data['user'] = current_user.id
        
        try:
            # Check if PrefredGender already exists for this user
            prefred_gender_instance = PrefredGender.objects.get(user=current_user)
            # If exists, update the existing record
            serializer = PrefredGenderSerializers(prefred_gender_instance, data=mutable_data)
        except PrefredGender.DoesNotExist:
            # If not, create a new record
            serializer = PrefredGenderSerializers(data=mutable_data)
        
        # Validate the serializer
        serializer.is_valid(raise_exception=True)
        
        # Save the instance (either create or update)
        serializer.save()

        # Return Response to User
        response = Response({
            'message': 'Prefred Gender Created/Updated Successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
        return response