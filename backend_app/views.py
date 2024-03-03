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

def csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

@csrf_exempt
def get_water_history(request):
    date_str = request.GET.get('date', None)

    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Date parameter is required.'}, status=400)
    

    start_date = date - timedelta(days=90)
    water_intake_records = WaterIntake.objects.filter(user__id=1, date__gte=start_date, date__lte=date).order_by('date')
    
    if not water_intake_records.exists():
        # If no records found, return an empty list
        return JsonResponse({'status': 'success', 'intake_records': []})

    # Convert the queryset to a list of dictionaries, one for each record
    intake_records = [
        {
            'date': record.date.strftime('%Y-%m-%d'),
            'water_amount': record.water_amount
        } for record in water_intake_records
    ]
    
    # Use safe=False for non-dict objects; since we're returning a list, it's required.
    return JsonResponse({'status': 'success', 'intake_records': intake_records}, safe=False)

@csrf_exempt
def get_fish_number(request):
    try:

        user_level = UserLevel.objects.get(user__id=1).level
    except UserLevel.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

    fish_numbers = {'level1_fish': 0, 'level2_fish': 0, 'level3_fish': 0, 'level4_fish': 0, 'level5_fish': 0}
    fish_numbers['level1_fish'] = user_level  

    for level in range(1, 5):
        while fish_numbers[f'level{level}_fish'] >= 3:
            fish_numbers[f'level{level}_fish'] -= 3
            fish_numbers[f'level{level+1}_fish'] += 1

    return JsonResponse({'status': 'success', 'fish_numbers': fish_numbers})

@csrf_exempt
@require_http_methods(["POST"])
def record_intake(request):
    try:
        data = json.loads(request.body)
        date = data['date']
        water_amount = data['water_amount']
        user_id = data['user_id']  
    except (ValueError, KeyError):
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

    User = get_user_model()
    try:
        user = User.objects.get(pk=1)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    
    WaterIntake.objects.create(user=user, date=date, water_amount=water_amount)
    
    return JsonResponse({'status': 'success', 'message': 'Water intake record created successfully'})

@csrf_exempt
@require_http_methods(["POST"])
def level_up(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        if not user_id:
            return JsonResponse({'status': 'error', 'message': 'User ID is required'}, status=400)
        
        updated_rows = UserLevel.objects.filter(user__id=user_id).update(level=F('level') + 1)
        
        if updated_rows:
            return JsonResponse({'status': 'success', 'message': 'User level up successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    