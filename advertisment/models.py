from django.db import models
from account.models import BaseModel
from django.utils import timezone
# Create your models here.

class Advertisment(BaseModel):
    video = models.FileField(null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    image1= models.ImageField(null=True,blank=True)
    image3= models.ImageField(null=True,blank=True)
    is_published = models.BooleanField(default=False)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    def save(self, *args, **kwargs):
            # Check if today's date is greater than the end date and if is_published is True
        if self.end_date and self.is_published and timezone.now().date() > self.end_date:
            self.is_published = False

        super(Advertisment, self).save(*args, **kwargs)
