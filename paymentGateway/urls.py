from django.urls import path,include
from .views import SubscriptionModelAPIview,PaymentGatewayAPIview

urlpatterns = [
     path('subscription-model/', SubscriptionModelAPIview.as_view(),name="SubscriptionModelAPIview"),
     path('subscription-model/<int:pk>/', SubscriptionModelAPIview.as_view(),name="SubscriptionModelAPIview"),
     
     path('payment/', PaymentGatewayAPIview.as_view(),name="PaymentGatewayAPIview"),
     path('payment/<int:pk>/', PaymentGatewayAPIview.as_view(),name="PaymentGatewayAPIview"),
     
]