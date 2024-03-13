from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from backend_app.models import UserLevel
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

# Create your views here.

### handle login logic using DRF. [mar 4, arthur]
# Endpoint: /api/login/
class LoginAPIView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated users to access this view for registration
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                    "token": token.key,
                    "username": user.username
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated users to access this view for registration

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password1 = request.data.get("password1")
        password2 = request.data.get("password2")
        
        form_data = {
            'username': username,
            'password1': password1,
            'password2': password2,  # Assuming the API doesn't separate password & confirmation
        }

        form = UserCreationForm(form_data)

        if form.is_valid():
            user = form.save()
            token, created = Token.objects.get_or_create(user=user)
            
            user_level = UserLevel(user=user, level=1)
            user_level.save()

            return Response({
                    "token": token.key,
                    "username": user.username
            }, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

