from django.urls import path,include
from .views import SubscriptionModelAPIview

urlpatterns = [
     path('subscription-model/', SubscriptionModelAPIview.as_view(),name="SubscriptionModelAPIview"),
     path('subscription-model/<int:pk>/', SubscriptionModelAPIview.as_view(),name="SubscriptionModelAPIview"),
]