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

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

# user record one record intake data, insert a line in WaterIntake Table
# data: user|date| water_amount
@api_view(['POST'])
@permission_classes([IsAuthenticated]) #only authorized users can write to database.
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
    permission_classes = [IsAuthenticated]
    @csrf_exempt
    def get(self, request):
        try:
            user_level = UserLevel.objects.get(user=request.user).level
        except UserLevel.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

        fish_numbers = {'level1_fish': 0, 'level2_fish': 0, 'level3_fish': 0, 'level4_fish': 0, 'level5_fish': 0}
        fish_numbers['level1_fish'] = user_level

        for level in range(1, 5):
            while fish_numbers[f'level{level}_fish'] >= 3:
                fish_numbers[f'level{level}_fish'] -= 3
                fish_numbers[f'level{level+1}_fish'] += 1

        return JsonResponse({'status': 'success', 'fish_numbers': fish_numbers})


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
        return JsonResponse({'status': 'error', 
                             'message': 'An error occurred: ' + str(e)}, 
                             status=400)
    

# end point:  \post_sync_level
#      -H "Authorization: Token YOURTOKEN" \
#      -H "Content-Type: application/json" \
#      -d '{"level": 2}'
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_sync_level(request):
    user = request.user
    requested_level = request.data.get('level')

    # if not provide a level data, the level will increase by ONE.
    if requested_level is None: # the level is 1 by default
        user_level, created = UserLevel.objects.get_or_create(user=user, defaults={'level': 1})#get 'level' from database
        user_level.level = user_level.level + 1 # level up
        user_level.save()
        return Response({'status': 'success', 
                         "message": "Level up successfully",
                         "level": user_level.level})

    try:# convert user input to integral data
        requested_level = int(requested_level)
    except ValueError:
        return Response({'status': 'error', 
                         "message": "Invalid level format, not an integral"}, 
                          status=status.HTTP_400_BAD_REQUEST)
    
    # check data range, the 'level' parameter must be >= 1
    if requested_level < 1:
        return Response({'status': 'error', 
                         "message": "Level must >= 1"}, 
                         status=status.HTTP_400_BAD_REQUEST)

    user_level, created = UserLevel.objects.get_or_create(user=user, defaults={'level': 1})#get 'level' from database
    
    if requested_level < user_level.level:
        return Response({'status': 'error',
                         "message": "Cannot decrease level", 
                         "level": user_level.level}, status=status.HTTP_403_FORBIDDEN)
    else:
        user_level.level = requested_level
        user_level.save()
        return Response({'status': 'success',
                         "message": "Level updated successfully", 
                         "level": user_level.level})

