# from django.shortcuts import render

# # Create your views here.
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import WaterIntake
# from .serializers import WaterIntakeSerializer

# class WaterIntakeCreateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         # Set user_id to 0 by default
#         request.data['user_id'] = 0
        
#         serializer = WaterIntakeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from datetime import datetime, timedelta
from django.utils import timezone
import json
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

from .models import UserLevel, WaterIntake
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.db.models import Sum
from django.db.models.functions import TruncDay
from datetime import timedelta


def csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})


@api_view(['POST'])
def record_intake(request):
    try:
        data = request.data
        date = data['date']
        water_amount = data['water_amount']
    except (ValueError, KeyError):
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
    WaterIntake.objects.create(user=request.user, date=date, water_amount=water_amount)
    return JsonResponse({'status': 'success', 'message': 'Water intake record created successfully'})

# fetch 3 days history data
# endpoint: /api/get_history_3days
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_3days_water_intake(request):
    """Create an endpoint to return the last 3 days of water intake data, aggregated by day."""
    today = timezone.now().date()
    a_week_ago = today - timezone.timedelta(days=3)
    data = WaterIntake.objects.filter(user=request.user, date__date__range=[a_week_ago, today]) \
                              .annotate(day=TruncDay('date')) \
                              .values('day') \
                              .annotate(total_ml=Sum('water_amount')) \
                              .order_by('day')

    if not data:
        return JsonResponse({'status': 'success', 'message': 'No water intake records found for the last 3 days', 'data': []})
    else:
        return JsonResponse({'status': 'success', 'data': list(data)})

# fetch weekly(last 7 dyas) history data
# endpoint: /api/get_history_weekly/
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_weekly_water_intake(request):
    """Create an endpoint to return the last 7 days of water intake data, aggregated by day."""
    today = timezone.now().date()
    a_week_ago = today - timezone.timedelta(days=7)
    data = WaterIntake.objects.filter(user=request.user, date__date__range=[a_week_ago, today]) \
                              .annotate(day=TruncDay('date')) \
                              .values('day') \
                              .annotate(total_ml=Sum('water_amount')) \
                              .order_by('day')

    if not data:
        return JsonResponse({'status': 'success', 'message': 'No water intake records found for the last 7 days', 'data': []})
    else:
        return JsonResponse({'status': 'success', 'data': list(data)})


# returns the monthly water intake data for the logged-in user.
# endpoint: /api/get_history_monthly/
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_monthly_water_intake(request):
    """Create an endpoint to return the last 30 days of water intake data, aggregated by day."""
    today = timezone.now().date()
    a_month_ago = today - timezone.timedelta(days=30)
    data = WaterIntake.objects.filter(user=request.user, date__date__range=[a_month_ago, today]) \
                              .annotate(day=TruncDay('date')) \
                              .values('day') \
                              .annotate(total_ml=Sum('water_amount')) \
                              .order_by('day')

    if not data:
        return JsonResponse({'status': 'success', 'message': 'No water intake records found for the last 30 days', 'data': []})
    else:
        return JsonResponse({'status': 'success', 'data': list(data)})


class GetFishNumber(APIView):
    permission_classes = [AllowAny]
    @csrf_exempt
    def get(self, request):
        return JsonResponse({'status': 'success', 'fish_numbers': 999})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def level_up(request):
    try:
        updated_rows = UserLevel.objects.filter(user=request.user).update(level=F('level') + 1)
        
        if updated_rows:
            return JsonResponse({'status': 'success', 'message': 'User level up successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    except Exception as e:  # Catching generic exception to handle unexpected errors
        return JsonResponse({'status': 'error', 'message': 'An error occurred: ' + str(e)}, status=400)
    