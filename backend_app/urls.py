# from django.urls import path
# from .views import WaterIntakeCreateAPIView

# urlpatterns = [
#     path('water-intake/', WaterIntakeCreateAPIView.as_view(), name='water_intake_create'),
# ]

from django.urls import path


from . import views

urlpatterns = [
    path("csrf/", views.csrf_token, name="csrf"),
    path("getwaterhistory/", views.GetWaterHistory.as_view(), name="waterintake"),
    path("getfishnumber/", views.GetFishNumber.as_view(), name="getfishnumber"),
    path("recordintake/", views.record_intake, name="recordwater"),
    path("levelup/", views.level_up, name="levelup"),
]