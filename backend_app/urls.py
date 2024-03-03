from django.urls import path
from .views import WaterIntakeCreateAPIView

urlpatterns = [
    path('water-intake/', WaterIntakeCreateAPIView.as_view(), name='water_intake_create'),
]