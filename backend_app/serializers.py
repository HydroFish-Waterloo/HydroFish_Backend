from rest_framework import serializers
from .models import WaterIntake

class WaterIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterIntake
        fields = ['date', 'amount']

class WaterHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterIntake
        fields = ['user', 'amount_ml', 'date_time']