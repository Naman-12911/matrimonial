from django.db import models
from account.models import User,BaseModel
# Create your models here.

class SubscriptionModel(BaseModel):
    model = models.CharField( max_length=100)
    price = models.BigIntegerField()
    description = models.TextField()
    
