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
from twilio.rest import Client
from django.conf import settings
from django.utils.crypto import get_random_string

class Register(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializers

    def generate_otp(self):
        return get_random_string(6, '0123456789')
    def send_otp_sms(self, phone_no, otp):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"This is your Second Inning Matrimonial.com OTP: {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_no
        )
        return message

    def post(self, request):
        user_data = request.data
        phone_no = user_data.get('phone_no')

        # Check if user with provided phone number already exists
        try:
            user = User.objects.get(phone_no=phone_no)
            already_exists = True
        except User.DoesNotExist:
            # If user does not exist, create a new user
            serializer = self.serializer_class(data=user_data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            already_exists = False

        # Generate and save OTP
        otp = self.generate_otp()
        OneTimePassword.objects.create(user=user, otp=otp)
        self.send_otp_sms(phone_no, otp)

        # Determine user type (existing or new)
      #  user_type = 'existing' if already_exists else 'new'

        # Return response with phone number, message, already_exits flag, and user type
        response_data = {
            'phone_no': phone_no,
            'message': 'OTP sent successfully and User is registered',
            'otp':otp,
            'already_exists': already_exists,
           # 'user_type': user_type
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

# otp verfication
    
class OTPVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPVerificationSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_no = serializer.validated_data.get('phone_no')
        otp = serializer.validated_data.get('otp')

        # Retrieve the user and the latest OTP instance
        user = User.objects.filter(phone_no=phone_no).first()
        otp_instance = OneTimePassword.objects.filter(user=user).order_by('-created_at').first()

        if not user or not otp_instance:
            return Response({'detail': 'Invalid phone number or OTP'}, status=status.HTTP_400_BAD_REQUEST)

        # Handle static OTP "000000" for bypass (if required)
        if otp == "000000":
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'phone_number': user.phone_no,
            }, status=status.HTTP_200_OK)

        # Check if the OTP is expired
        if otp_instance.is_expired:
            return Response({'detail': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the OTP
        if otp == otp_instance.otp:
            # Mark OTP as expired
            otp_instance.expired = True
            otp_instance.save()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'phone_number': user.phone_no,
            }, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
    

# resend OTP verification code
class ResendOTPAPIview(APIView):
    permission_classes = [AllowAny]

    def generate_otp(self):
        return get_random_string(6, '0123456789')

    def send_otp_sms(self, phone_no, otp):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"This is your Second Inning Matrimonial.com  OTP: {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_no
        )
        return message

    def post(self, request):
        phone_no = request.data.get('phone_no')
        
        # Check if the phone number exists in the database
        user = User.objects.filter(phone_no=phone_no).first()
        if not user:
            return Response({'detail': 'User with this phone number does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a new OTP
        new_otp = self.generate_otp()
        OneTimePassword.objects.create(user=user, otp=new_otp)
        self.send_otp_sms(phone_no, new_otp)

        # Send the OTP to the user's phone number (implement this part)

        return Response({'detail': 'New OTP sent successfully'}, status=status.HTTP_200_OK)
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