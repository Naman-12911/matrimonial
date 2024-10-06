from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from account.managers import CustomUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)
RELIGION_CHOICES = [
    ('Islam', 'Islam'),
    ('Christianity', 'Christianity'),
    ('Hinduism', 'Hinduism'),
    ('Buddhism', 'Buddhism'),
    ('Sikhism', 'Sikhism'),
    ('Judaism', 'Judaism'),
    ('Atheism', 'Atheism'),
    ('Agnosticism', 'Agnosticism'),
    ('Other', 'Other'),
]
FAMILY_TYPE_CHOICES = [
    ('Nuclear Family', 'Nuclear Family'),
    ('Joint Family', 'Joint Family'),
    ('UpperMiddle Class Family', 'Upper Middle Class Family'),
    ('Middle Family', 'Middle Class Family'),
    ('Affluent Family', 'Affluent Family'),
    ('Business Family', 'Business Family'),
    ('Liberal Family', 'Liberal Family'),
    ('Conservative Family', 'Conservative Family'),
    ('Religious Family', 'Religious Family'),
    ('Rich Family', 'Rich Family'),
    ('Moderate Family', 'Moderate Family'),
]
# Cast Choices
CAST_CHOICES = [
    ('Brahmin', 'Brahmin'),
    ('Kshatriya', 'Kshatriya'),
    ('Vaishya', 'Vaishya'),
    ('Shudra', 'Shudra'),
    ('Scheduled Caste (SC)', 'Scheduled Caste (SC)'),
    ('Scheduled Tribe (ST)', 'Scheduled Tribe (ST)'),
    ('Other', 'Other'),
]

# Sub-Cast Choices
SUB_CAST_CHOICES = [
    # Sub-castes for Brahmin
    ('Iyer', 'Iyer'),
    ('Iyengar', 'Iyengar'),
    ('Saraswat', 'Saraswat'),
    ('Gaur', 'Gaur'),
    
    # Sub-castes for Kshatriya
    ('Rajput', 'Rajput'),
    ('Maratha', 'Maratha'),
    ('Jat', 'Jat'),

    # Sub-castes for Vaishya
    ('Agarwal', 'Agarwal'),
    ('Gupta', 'Gupta'),
    ('Khandelwal', 'Khandelwal'),

    # Sub-castes for Scheduled Caste (SC)
    ('Mahar', 'Mahar'),
    ('Chamar', 'Chamar'),
    ('other','other')

    # Add more as needed
]

SMOKE__DRINK_CHOICE = [
    ('occasionally', 'occasionally'),
    ('Regularly', 'Regularly'),
    ('No', 'No'),
]

AUTH_PROVIDERS = {'google': 'google','phone_no':'phone_no'}
class User(AbstractUser):
    username = None
    # email = models.EmailField(_('email address'), unique=True)
    # own Profile
    phone_no = models.CharField(blank=True,unique=True,max_length=15)
    is_verified = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)  # Gender field with choices
    height = models.FloatField(null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    location = models.CharField(max_length=100,null=True,blank=True)
    religion = models.CharField(max_length=100,choices=RELIGION_CHOICES,null=True,blank=True)
    cast = models.CharField(max_length=100,null=True,blank=True)
    sub_cast = models.CharField(max_length=100,null=True,blank=True)
    income = models.BigIntegerField(null=True,blank=True)
    bio = models.TextField(null=True,blank=True)
    family_background = models.TextField(null=True,blank=True)
    family_type = models.CharField(max_length=100,choices=FAMILY_TYPE_CHOICES,null=True,blank=True)
    
    photo1 = models.ImageField(null=True,blank=True)
    photo2 = models.ImageField(null=True,blank=True)
    photo3 = models.ImageField(null=True,blank=True)
    photo4 = models.ImageField(null=True,blank=True)
    photo5 = models.ImageField(null=True,blank=True)
    date_of_birth = models.CharField(max_length=100,null=True,blank=True)
    job_about = models.CharField(max_length=100,null=True,blank=True)
    buiness_about = models.CharField(max_length=100,null=True,blank=True)
    job = models.BooleanField(default=False)
    buiness = models.BooleanField(default=False)
    # smoke = models.BooleanField(default=False)
    # drink = models.BooleanField(default=False)
    smoke = models.CharField(max_length=15, choices=SMOKE__DRINK_CHOICE, blank=True) 
    drink = models.CharField(max_length=15, choices=SMOKE__DRINK_CHOICE, blank=True)  
    is_profile_created = models.BooleanField(default=False)
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
    def get_photo_url(self, photo_field,request):
        if photo_field:
            return request.build_absolute_uri(f"{settings.MEDIA_URL}{photo_field}")
        return None

    @property
    def photo1_url(self):
        return self.get_photo_url(self.photo1, self._request)

    @property
    def photo2_url(self):
        return self.get_photo_url(self.photo1, self._request)

    @property
    def photo3_url(self):
        return self.get_photo_url(self.photo1, self._request)

    @property
    def photo4_url(self):
        return self.get_photo_url(self.photo1, self._request)

    @property
    def photo5_url(self):
        return self.get_photo_url(self.photo1, self._request)

    def set_request(self, request):
        self._request = request
    
class PrefredGender(models.Model):
    user = models.OneToOneField(User,models.CASCADE,null=True,blank=True)
    prefred_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True,null=True)  # Gender field with choices
    prefred_height = models.FloatField(null=True,blank=True)
    prefred_location = models.CharField(max_length=100,null=True,blank=True)
    prefred_religion = models.CharField(max_length=100,choices=RELIGION_CHOICES,null=True,blank=True)
    prefred_income = models.BigIntegerField(null=True,blank=True)
    family_type = models.CharField(max_length=100,choices=FAMILY_TYPE_CHOICES,null=True,blank=True)
    # prefred_smoke = models.BooleanField(default=False)
    # prefred_drink = models.BooleanField(default=False)
    prefred_smoke = models.CharField(max_length=15, choices=SMOKE__DRINK_CHOICE, blank=True) 
    prefred_drink = models.CharField(max_length=15, choices=SMOKE__DRINK_CHOICE, blank=True)
    cast = models.CharField(max_length=100,choices=CAST_CHOICES,null=True,blank=True)
    sub_cast = models.CharField(max_length=100,choices=SUB_CAST_CHOICES,null=True,blank=True)
    
class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    
class OneTimePassword(BaseModel):
    otp = models.CharField(max_length=6, blank=True, null=True)
    expired = models.BooleanField(default=False)
    @property
    def is_expired(self):
        return self.expired or (timezone.now() > self.created_at + timezone.timedelta(minutes=2))