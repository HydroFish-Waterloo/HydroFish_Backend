from django.shortcuts import render

# Create your views here.
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