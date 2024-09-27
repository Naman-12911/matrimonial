from rest_framework import serializers
import random
from account.models import User
from paymentGateway.models import PaymentGateway
from .models import Swipe

class UserSerializers(serializers.ModelSerializer):
    phone_no = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = "__all__"

    def get_phone_no(self, obj):
        # Check if the logged-in user has a paid membership
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                # Check if the logged-in user has a paid membership
                current_user_payment = PaymentGateway.objects.get(user=request.user)
                if current_user_payment.paid_member:
                    return obj.phone_no  # Show full phone number if logged-in user is a paid member
            except PaymentGateway.DoesNotExist:
                pass
        
        # Mask phone number for non-paying members
        if obj.phone_no:
            return f"{obj.phone_no[:2]}****{obj.phone_no[-2:]}"
        return None

    def get_email(self, obj):
        # Check if the logged-in user has a paid membership
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                # Check if the logged-in user has a paid membership
                current_user_payment = PaymentGateway.objects.get(user=request.user)
                if current_user_payment.paid_member:
                    return obj.email  # Show full email if logged-in user is a paid member
            except PaymentGateway.DoesNotExist:
                pass

        # Mask email for non-paying members
        if obj.email:
            name, domain = obj.email.split('@')
            masked_name = f"{name[0]}{'*' * (len(name) - 2)}{name[-1]}"
            return f"{masked_name}@{domain}"
        return None
    
class SwipeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Swipe
        fields = "__all__"