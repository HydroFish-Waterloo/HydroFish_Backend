from django.urls import re_path, path
from django.contrib.auth.views import LoginView

from . import views
## import from my code
from .views import LoginAPIView, RegisterAPIView

#app_name = 'users'

urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='api_login'), #api for mobile app. [mar 4]
    path('api/register/', RegisterAPIView.as_view(), name='api_register'), #api for mobile app. [mar 5]
]
