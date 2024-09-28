
from .models import SubscriptionModel,PaymentGateway
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken

class SubscriptionModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionModel
        fields = "__all__"
        

class PaymentGatewaySerializers(serializers.ModelSerializer):
    class Meta:
        model = PaymentGateway
        fields = "__all__"