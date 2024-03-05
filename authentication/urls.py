from django.urls import re_path, path
from django.contrib.auth.views import LoginView

from . import views
from .views import LoginAPIView

#app_name = 'users'

urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='api_login'), #api for mobile app. [mar 4]
]
