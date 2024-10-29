from . import models
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken

# register serializers
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['phone_no','is_verified','gender','height','name','location','religion','cast','sub_cast','income',
                  'bio','family_background','family_type','photo1','photo2','photo3','photo4','photo5','date_of_birth','job_about',
                  'buiness_about','job','buiness','medical_history','medical_history_if_any','smoke','drink','is_profile_created']

    def get_photo1_url(self, obj):
        request = self.context.get('request')
        obj.set_request(request)  
        return obj.photo1_url

    def get_photo2_url(self, obj):
        request = self.context.get('request')
        obj.set_request(request)  
        return obj.photo2_url

    def get_photo3_url(self, obj):
        request = self.context.get('request')
        obj.set_request(request)  
        return obj.photo3_url
    def get_photo4_url(self, obj):
        request = self.context.get('request')
        obj.set_request(request)  
        return obj.photo4_url
    def get_photo5_url(self, obj):
        request = self.context.get('request')
        obj.set_request(request)  
        return obj.photo5_url
    

class UserLoginSerializer(serializers.ModelSerializer):
    phone_no = serializers.CharField(max_length=12, min_length=3)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = models.User.objects.get(phone_no=obj['phone_no'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = models.User
        fields = ['phone_no', 'tokens',]

    def validate(self, attrs):
        phone_no = attrs.get('phone_no', '')

        filtered_user_by_phone_no = models.User.objects.filter(phone_no=phone_no)
        user = auth.authenticate(phone_no=phone_no,)

        if filtered_user_by_phone_no.exists() and filtered_user_by_phone_no[0].auth_provider != 'phone_no':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_phone_no[0].auth_provider)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        
        if user.auth_provider != 'phone_no':
            raise AuthenticationFailed(f'Please continue your login using {user.auth_provider}')

        return {
            'phone_no': user.phone_no,
            'tokens': user.tokens,         
        }

        return super().validate(attrs)
    
class OTPVerificationSerializers(serializers.Serializer):
    phone_no = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)

    
class PrefredGenderSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.PrefredGender
        fields = "__all__"