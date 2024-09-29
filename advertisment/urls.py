from django.urls import path,include
from .views import AdvertismentAPIview

urlpatterns = [
     path('advertisment/', AdvertismentAPIview.as_view(),name="AdvertismentAPIview"),
     path('advertisment/<int:pk>/', AdvertismentAPIview.as_view(),name="AdvertismentAPIview"),

     
]