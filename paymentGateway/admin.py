from django.contrib import admin
from .models import SubscriptionModel,PaymentGateway
# Register your models here.

admin.site.register(SubscriptionModel)
admin.site.register(PaymentGateway)