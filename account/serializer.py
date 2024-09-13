from . import models
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken

# register serializers
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"
        extra_kwargs = {
            'password' :{'write_only':True}  #  to does not return password in api ## postman
        }
    # convert password to hash key
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        if len(password) <6:
            raise serializers.ValidationError("entre strong password")
        instance.save()
        return instance
    

class UserLoginSerializer(serializers.ModelSerializer):
    phone_no = serializers.CharField(max_length=12, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = models.User.objects.get(phone_no=obj['phone_no'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = models.User
        fields = "__all__"

    def validate(self, attrs):
        phone_no = attrs.get('phone_no', '')
        password = attrs.get('password', '')
        filtered_user_by_phone_no = models.User.objects.filter(phone_no=phone_no)
        user = auth.authenticate(phone_no=phone_no, password=password)

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
            'email': user.email,
            'tokens': user.tokens,         
        }

        return super().validate(attrs)