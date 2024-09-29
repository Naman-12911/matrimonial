from django.urls import path,include
from .views import Register,userData,update_profile,PrefredGenderAPIview,OTPVerificationView,ResendOTPAPIview

urlpatterns = [
     path('register/', Register.as_view(),name="register"),
     path('verify-otp/', OTPVerificationView.as_view(), name='OTPVerificationView'),
     path('resend-otp/', ResendOTPAPIview.as_view(), name='ResendOTPAPIview'),
     path('profile/',userData.as_view(),name="profile"),
     path('update-profile/',update_profile.as_view(),name="update_profile"),
     path('prefrence/',PrefredGenderAPIview.as_view(),name="PrefredGenderAPIview"),
     path('user-data/',userData.as_view(),name="userData"),
]