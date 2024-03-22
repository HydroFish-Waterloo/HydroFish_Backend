# from django.urls import path
# from .views import WaterIntakeCreateAPIView

# urlpatterns = [
#     path('water-intake/', WaterIntakeCreateAPIView.as_view(), name='water_intake_create'),
# ]

from django.urls import path


from . import views

urlpatterns = [
    path("csrf/", views.csrf_token, name="csrf"),

    ## for 'main' page
    path("recordintake/", views.record_intake, name="recordwater"),
    path("getfishnumber/", views.GetFishNumber.as_view(), name="getfishnumber"),
    path("levelup/", views.level_up, name="levelup"),
    
    ## for 'history' page
    path("get_history_3days/", views.get_3days_water_intake, name="get_3days_water_intake"), #get 3-days data (all are most recent days)
    path("get_history_weekly/", views.get_weekly_water_intake, name="get_weekly_water_intake"), #get 7-days data
    path("get_history_monthly/", views.get_monthly_water_intake, name="get_monthly_water_intake"),#get 30-days data

    ## for 'settings' page
    path("getsettings/", views.get_settings, name="get_settings"),
    path("setsettings/", views.set_settings, name="set_settings"),

]