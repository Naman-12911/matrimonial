from django.urls import path
from .views import MatchedProfilesView,SwipeOrMatchAPIview

urlpatterns = [
    path('matched-profiles/', MatchedProfilesView.as_view(), name='matched-profiles'),
    path('matched-profiles/<int:pk>/', MatchedProfilesView.as_view(), name='matched-profiles'),
    path('swipe/', SwipeOrMatchAPIview.as_view(), name='SwipeOrMatchAPIview'),
    path('swipe/<int:pk>/', SwipeOrMatchAPIview.as_view(), name='SwipeOrMatchAPIview'),
]
