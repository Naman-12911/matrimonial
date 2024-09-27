from django.db import models
from account.models import BaseModel,User
# Create your models here.

class Swipe(BaseModel):
    liked_person = models.ForeignKey(User,models.CASCADE,null=True,blank=True)
