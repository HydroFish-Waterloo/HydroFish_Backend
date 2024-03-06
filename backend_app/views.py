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

def csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

class GetWaterHistory(APIView):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get(self, request):
        date_str = request.GET.get('date', None)

        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({'status': 'error', 'message': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'Date parameter is required.'}, status=400)

        start_date = date - timedelta(days=90)
        end_date = datetime.combine(date, datetime.max.time())
        water_intake_records = WaterIntake.objects.filter(
            user=request.user, 
            date__gte=start_date, 
            date__lte=end_date
        ).order_by('date')
                
        if not water_intake_records.exists():
            return JsonResponse({'status': 'success', 'intake_records': []})

        intake_records = [
            {
                'date': record.date.strftime('%Y-%m-%d'),
                'water_amount': record.water_amount
            } for record in water_intake_records
        ]
        
        return JsonResponse({'status': 'success', 'intake_records': intake_records}, safe=False)

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
def record_intake(request):
    try:
        data = request.data
        date = data['date']
        water_amount = data['water_amount']
    except (ValueError, KeyError):
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

    WaterIntake.objects.create(user=request.user, date=date, water_amount=water_amount)
    
    return JsonResponse({'status': 'success', 'message': 'Water intake record created successfully'})

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
    