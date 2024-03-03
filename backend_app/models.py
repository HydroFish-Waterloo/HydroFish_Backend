from django.db import models

class WaterIntake(models.Model):
    user_id = models.IntegerField()
    date = models.DateField()
    amount = models.FloatField()

class WaterLevel(models.Model):
    user_id = models.IntegerField()
    level = models.IntegerField()

class Fish(models.Model):
    user_id = models.IntegerField()
    fish_count = models.IntegerField()

class Notification(models.Model):
    user_id = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    interval = models.IntegerField()