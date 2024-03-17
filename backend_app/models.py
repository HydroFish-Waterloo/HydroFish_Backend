from django.db import models
from django.conf import settings

class WaterIntake(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField()
    water_amount = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.water_amount} liters"

class UserLevel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - Level {self.level}"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    wakeup_time = models.TimeField()
    sleep_time = models.TimeField()
    interval = models.IntegerField(help_text="Interval in minutes")

    def __str__(self):
        return f"{self.user.username} - Notification Settings"