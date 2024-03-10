# from django.urls import path
# from .views import WaterIntakeCreateAPIView

# urlpatterns = [
#     path('water-intake/', WaterIntakeCreateAPIView.as_view(), name='water_intake_create'),
# ]

from django.urls import path


from . import views

urlpatterns = [
    path("csrf/", views.csrf_token, name="csrf"),

    path("recordintake/", views.record_intake, name="recordwater"),

    ## for 'history' page
    path("get_history_3days/", views.get_3days_water_intake, name="get_3days_water_intake"),
    path("get_history_weekly/", views.get_weekly_water_intake, name="get_weekly_water_intake"),
    path("get_history_monthly/", views.get_monthly_water_intake, name="get_monthly_water_intake"),

    path("getfishnumber/", views.GetFishNumber.as_view(), name="getfishnumber"),
    path("levelup/", views.level_up, name="levelup"),
]