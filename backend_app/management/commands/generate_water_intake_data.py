# Generate random but reasonable data within the constraints
# (e.g., several intakes per day with a total daily intake of about 2000ml to 4000ml).

############### HOW TO USE THIS SCRIPT ##################
# to run, use this:
# python manage.py generate_water_intake_data
# ( Ensure you have a user with the username 'arthur2' in your database, or create one if it doesn't exist.)
######################################################

# This script:
# Retrieves the user with username 'arthur2'.
# Generates one month of water intake data, ensuring each day has a total intake of at least 2000ml, spread across several intakes between 6 AM and 10 PM.
# Randomizes the amount of each intake to simulate realistic behavior.

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
import random
from backend_app.models import WaterIntake

class Command(BaseCommand):
    help = 'Generate one month of water intake data for user "arthur2"'

    def handle(self, *args, **kwargs):
        # Assuming you have a user with username 'arthur2'
        name='arthur3'
        password='147258@@@'

        User = get_user_model()
        # Check if the user exists, otherwise create it
        user, created = User.objects.get_or_create(username= name)
        if created:
            user.set_password(password)  # Set the password for the new user
            user.save()
            print('### User "', name , '", password=' , password, '. created OK.')
        else:
            print('### User "', name , '" already exists, no need to creat.')

        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=30)
        
        how_many_days = 60
        for day in range(how_many_days):  # Generate data for each day in the month
            day_date = start_date + timedelta(days=day)
            daily_total = 0
            while daily_total < 2000:  # Ensure at least 2000ml intake per day
                intake_time = day_date + timedelta(hours=random.randint(6, 22), minutes=random.randint(0, 59))
                intake_amount = random.randint(200, 700)  # Each intake between 200ml and 700ml
                WaterIntake.objects.create(user=user, date=make_aware(intake_time), water_amount=intake_amount)
                daily_total += intake_amount

        print('### Successfully generated water intake data for recent ', f'{how_many_days}', 'days.')


