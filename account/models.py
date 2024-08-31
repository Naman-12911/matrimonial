from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from account.managers import CustomUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.contrib.auth.models import User

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

AUTH_PROVIDERS = {'google': 'google','phone_no':'phone_no'}
class User(AbstractUser):
    username = None
    # email = models.EmailField(_('email address'), unique=True)
    phone_no = models.CharField(blank=True,unique=True,max_length=12)
    is_verified = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)  # Gender field with choices
    height = models.FloatField(null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    prefrence = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    location = models.CharField(max_length=100,null=True,blank=True)
    photo1 = models.ImageField(null=True,blank=True)
    photo2 = models.ImageField(null=True,blank=True)
    photo3 = models.ImageField(null=True,blank=True)
    photo4 = models.ImageField(null=True,blank=True)
    photo5 = models.ImageField(null=True,blank=True)
    date_of_birth = models.CharField(max_length=100,null=True,blank=True)
    job = models.CharField(max_length=100,null=True,blank=True)
    smoke = models.BooleanField(default=False)
    drink = models.BooleanField(default=False)
    bio = models.TextField(null=True,blank=True)
    auth_provider = models.CharField(max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get('phone_no'))
    USERNAME_FIELD = 'phone_no'
    objects = CustomUserManager() 
    REQUIRED_FIELDS = []
    def __str__(self):
        return str(self.phone_no)
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    def get_photo_url(self, photo_field):
        if photo_field:
            return f"{settings.MEDIA_URL}{photo_field}"
        return None

    @property
    def photo1_url(self):
        return self.get_photo_url(self.photo1)

    @property
    def photo2_url(self):
        return self.get_photo_url(self.photo2)

    @property
    def photo3_url(self):
        return self.get_photo_url(self.photo3)

    @property
    def photo4_url(self):
        return self.get_photo_url(self.photo4)

    @property
    def photo5_url(self):
        return self.get_photo_url(self.photo5)