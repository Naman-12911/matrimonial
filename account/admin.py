from django.contrib import admin
# Register your models here.
from django.utils.translation import gettext_lazy  as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User,OneTimePassword,PrefredGender


class customUserAdmin(UserAdmin):
  #form = UserChangeForm
  fieldsets = (
      (None, {'fields': ('email', 'password', )}),
      (_('Personal info'), {'fields': ('name',)}),
      (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser'
                                                ),}),
      (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('user_info'), {'fields': ( 'phone_no',
                                     )}),

       (_('account_info'), {'fields': ( 'is_verified','gender','height',
                                       'location','photo1','photo2','photo3','photo4','photo5',"date_of_birth",'job','smoke','drink','bio',
                                       'religion', 'income','family_background','family_type','job_about' ,'buiness_about' ,'is_profile_created','medical_history','medical_history_if_any',
                                     )}),
  )
  add_fieldsets = (
      (None, {
          'classes': ('wide', ),
          'fields': ('phone_no',),
      }),
  )
  list_display = ['phone_no', 'name', 'is_staff']
  search_fields = ('phone_no',)
  ordering = ('phone_no', )
admin.site.register(User, customUserAdmin)
admin.site.unregister(Group)
admin.site.register(OneTimePassword)
admin.site.register(PrefredGender)