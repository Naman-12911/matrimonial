from django.urls import path
from .views import MatchedProfilesView

urlpatterns = [
    path('matched-profiles/', MatchedProfilesView.as_view(), name='matched-profiles'),
    path('matched-profiles/<int:pk>/', MatchedProfilesView.as_view(), name='matched-profiles'),
]
