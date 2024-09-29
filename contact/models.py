from django.db import models
from account.models import BaseModel
# Create your models here.

class ContactUs(BaseModel):
    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    phone_no = models.CharField(max_length=100,null=True,blank=True)
    content = models.TextField(null=True,blank=True)
