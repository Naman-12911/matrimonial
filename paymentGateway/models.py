from django.db import models
from account.models import User,BaseModel
from django.utils import timezone
# Create your models here.

class SubscriptionModel(BaseModel):
    model = models.CharField( max_length=100)
    price = models.BigIntegerField(null=True,blank=True)
    description = models.TextField()
    

class PaymentGateway(models.Model):
    user = models.OneToOneField(User,models.CASCADE,null=True,blank=True)
    subscription_type = models.ForeignKey(SubscriptionModel,models.CASCADE,null=True,blank=True)
    paid_member = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)