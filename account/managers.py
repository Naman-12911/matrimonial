from django.core.validators import validate_integer
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_no, password, **extra_fields):
        if not phone_no:
            raise ValueError(_("The phone number must be set"))

        try:
            validate_integer(phone_no)
        except ValidationError:
            raise ValueError(_("Invalid phone number"))

        user = self.model(phone_no=phone_no, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_no, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(phone_no, password, **extra_fields)