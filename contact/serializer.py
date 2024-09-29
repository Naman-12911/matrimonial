
from .models import ContactUs
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken

class ContactUsSerializers(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"
        

