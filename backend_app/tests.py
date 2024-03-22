from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient

from .models import UserLevel, WaterIntake, Notification


class WaterIntakeTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.test_user = User.objects.create_user(username='testuser', password='testpassword123')
        # Create a token for the test user
        self.token = Token.objects.create(user=self.test_user)
        # Set the token in the header for authentication
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('recordwater') # the URL for the record_intake endpoint

    def test_record_intake_success(self):
        
        # Data to be sent in request
        data = {
            'date': '2022-03-04',
            'water_amount': 500
        }
        # Make the POST request
        response = self.client.post(self.url, data, format='json')
        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if exactly one line of record has been created
        self.assertEqual(WaterIntake.objects.count(), 1)
        # Check if the 'user' filed of the newly created record matches the 'user' objets
        self.assertEqual(WaterIntake.objects.get().user, self.test_user)

        # Optionally, check the response content
        self.assertEqual(response.json(), {'status': 'success', 
                                         'message': 'Water intake record created successfully'})

        data = {
            'date': '2022-03-04',
            'water_amount': 500,
            'water_amount': 600,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(WaterIntake.objects.count(), 2) #this is the 2nd record.

    def test_record_intake_failure(self):
        """1 Test data is not provided."""
        data = ''
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(WaterIntake.objects.count(), 0)

        """2 Test missing some part."""
        """Test ."""
        data = {'water_amount': 500} #missing 1st one
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(WaterIntake.objects.count(), 0)

        data = {'data': '2022-03-04'} #missing 2nd one
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(WaterIntake.objects.count(), 0)


        """3 Test some part(s) is wrong."""
        data = {
            'date1': '2022-03-04',
            'water_amount': 500 #this part is wrong
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(WaterIntake.objects.count(), 0)

        data = {
            'date': '2022-03-04',
            'water_amount_': 500  #this part is wrong
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(WaterIntake.objects.count(), 0)

        data = {
            'date': '03-04-2022', #date format is wrong
            'water_amount': 500
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(WaterIntake.objects.count(), 0)   

        data = {
            'date1': '2022-03-04',
            'water_amount': '500' # water amount should be an integer 
        }
        response = self.client.post(self.url, data, format='json')     
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(WaterIntake.objects.count(), 0)        

        """Test has some extra part(s)."""
        data = {
            'date': '2022-03-04',
            'water_amount': 500,
            'wrong_field': 'some_value'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(WaterIntake.objects.count(), 0)


class GetWaterIntakeTests(TestCase):
    def setUp(self):
        # Create a test user
        self.test_user = User.objects.create_user(username='testuser1', password='testpassword123')
        # Create a token for the test user
        self.token = Token.objects.create(user=self.test_user)
        # Set the token in the header for authentication
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.url1 = reverse('get_3days_water_intake') # the URL for the record_intake endpoint
        self.url2 = reverse('get_weekly_water_intake') # the URL for the record_intake endpoint
        self.url3 = reverse('get_monthly_water_intake') # the URL for the record_intake endpoint
        

    def create_water_intake_records(self, user):
        # Create some water intake records for the last 30 days
        for days_ago in range(1, 31):
            date = timezone.now() - timezone.timedelta(days=days_ago)
            WaterIntake.objects.create(user=user, date=date, water_amount=1000)  # 1000 ml for simplicity

    def test_get_monthly_water_intake_failure(self):
        # Make a GET request to the endpoint
        response = self.client.get(self.url3)
        # Assert the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert the response data length is 30 (for the last 30 days)
        self.assertEqual(len(response.json()['data']), 0)
        
    def test_get_monthly_water_intake_ok(self):
        # Create WaterIntake records
        self.create_water_intake_records(self.test_user)

        # Make a GET request to the endpoint
        response = self.client.get(self.url1)
        # Assert the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert the response data length is 30 (for the last 30 days)
        self.assertEqual(len(response.json()['data']), 3)

        # Make a GET request to the endpoint
        response = self.client.get(self.url2)
        # Assert the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert the response data length is 30 (for the last 30 days)
        self.assertEqual(len(response.json()['data']), 7)

        # Make a GET request to the endpoint
        response = self.client.get(self.url3)
        # Assert the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert the response data length is 30 (for the last 30 days)
        self.assertEqual(len(response.json()['data']), 30)


class GetFishNumberTests(TestCase):
    def setUp(self):
        # Create a test user
        self.test_user = User.objects.create_user(username='testuser2', password='testpassword123')
        # Create a token for the test user
        self.token = Token.objects.create(user=self.test_user)
        # Set the token in the header for authentication
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.url = reverse('getfishnumber') # the URL for the record_intake endpoint

    def create_user_level(self, level):
        # Helper function to create UserLevel
        return UserLevel.objects.create(user=self.test_user, level=level)

    def update_user_level(self, new_level):
        # Helper fucntion to Update the level of the test user's UserLevel instance.
        # Retrieve the UserLevel instance for the test user
        user_level, created = UserLevel.objects.get_or_create(user=self.test_user)
        # Update the level
        user_level.level = new_level
        user_level.save()
        return user_level    

    def test_exit_first_return(self): # when there is no data in database
        """No user level in database, error returned """
        # Make a GET request to the endpoint
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404) 
        self.assertEqual(response.json(), {'status': 'error', 'message': 'User not found'})

    def test_get_fish_numbers_level_1(self):
        """test getting database data ok """
        self.create_user_level(level=1) # Create a UserLevel instance
        # Make a GET request to the endpoint
        response = self.client.get(self.url)
        # Assert the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expected fish numbers for level 1
        expected_fish_numbers = {'level1_fish': 1, 
                                 'level2_fish': 0, 
                                 'level3_fish': 0, 
                                 'level4_fish': 0, 
                                 'level5_fish': 0}
        # Assert the response fish_numbers match the expected values
        self.assertEqual(response.json()['fish_numbers'], expected_fish_numbers)

    def test_get_fish_numbers_level_others(self):
        """test the level up function """
        """level =3 """
        self.create_user_level(level=3) # Create a UserLevel instance
        # Make a GET request to the endpoint
        response = self.client.get(self.url)
        # Assert the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expected fish numbers for level 
        expected_fish_numbers = {'level1_fish': 0, 
                                 'level2_fish': 1, 
                                 'level3_fish': 0, 
                                 'level4_fish': 0, 
                                 'level5_fish': 0}
        # Assert the response fish_numbers match the expected values
        self.assertEqual(response.json()['fish_numbers'], expected_fish_numbers)

        """level =4 """
        self.update_user_level(4)    # Create a UserLevel instance
        # Make a GET request to the endpoint
        response = self.client.get(self.url)
        # Assert the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expected fish numbers for level 
        expected_fish_numbers = {'level1_fish': 1, 
                                 'level2_fish': 1, 
                                 'level3_fish': 0, 
                                 'level4_fish': 0, 
                                 'level5_fish': 0}
        # Assert the response fish_numbers match the expected values
        self.assertEqual(response.json()['fish_numbers'], expected_fish_numbers)

        """level = 10 """
        self.update_user_level(10)    # Create a UserLevel instance
        # Make a GET request to the endpoint
        response = self.client.get(self.url)
        # Assert the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expected fish numbers for level 
        expected_fish_numbers = {'level1_fish': 1, 
                                 'level2_fish': 0, 
                                 'level3_fish': 1, 
                                 'level4_fish': 0, 
                                 'level5_fish': 0}
        # Assert the response fish_numbers match the expected values
        self.assertEqual(response.json()['fish_numbers'], expected_fish_numbers)

        """level = 1000 """
        self.update_user_level(1000)    # Create a UserLevel instance
        # Make a GET request to the endpoint
        response = self.client.get(self.url)
        # Assert the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expected fish numbers for level 
        expected_fish_numbers = {'level1_fish': 1, 
                                 'level2_fish': 0, 
                                 'level3_fish': 0, 
                                 'level4_fish': 1, 
                                 'level5_fish': 12}
        # Assert the response fish_numbers match the expected values
        self.assertEqual(response.json()['fish_numbers'], expected_fish_numbers)


# The test will cover various scenarios
# 1- The level is not provided.
# 2- The level is in an invalid format (not an integer).
# 3- The level is less than 1.
# 4- The requested level is less than the current level in the backend.
# 5- The requested level is greater than or equal to the current level in the backend.
class LevelUpTests(APITestCase):
    def setUp(self):
        # Create a test user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        # URL for the level_up endpoint
        self.url = reverse('level_up')  #

    def create_user_level(self, level=1):
        # Helper function to create UserLevel
        return UserLevel.objects.create(user=self.user, level=level)

    def test_level_not_provided(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "'level' is not provided")

    def test_invalid_level_format(self):
        response = self.client.post(self.url, {'level': 'invalid'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Invalid level format, not an integral")

    def test_level_less_than_one(self):
        response = self.client.post(self.url, {'level': 0}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "'level' must >= 1")

    def test_requested_level_lower_than_current(self):
        self.create_user_level(level=5)
        response = self.client.post(self.url, {'level': 3}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Front has a lower level than backend, return value in backend.")

    def test_update_level_successfully(self):
        self.create_user_level(level=1)
        response = self.client.post(self.url, {'level': 5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "'level' updated successfully")
        self.assertEqual(response.data['level'], 5)


## test get/set settings, using path coverage stratage
class SettingsTests(APITestCase):
    def setUp(self):
        # Create a test user and a token for authentication
        self.user = User.objects.create_user('testuser', 'testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        # URLs for endpoints
        self.set_settings_url = reverse('set_settings')
        self.get_settings_url = reverse('get_settings')

    def test_set_settings_success(self):
        """Test successfully setting user notification settings."""
        data = {'wakeup_time': '07:00:00', 
                'sleep_time': '23:00:00', 
                'interval': 60}
        response = self.client.post(self.set_settings_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.wakeup_time.strftime('%H:%M:%S'), data['wakeup_time'])
        self.assertEqual(notification.sleep_time.strftime('%H:%M:%S'), data['sleep_time'])
        self.assertEqual(notification.interval, data['interval'])

    def test_set_settings_failure(self):
        """Test response when having exceptions"""
        data = {'wakeup_time': '07:00:00', 
                'sleep_time': '23:00:00'}
               # 'interval': '60'}  #test missing one required parameter
        response = self.client.post(self.set_settings_url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Notification.objects.count(), 0)

        data = {'wakeup_time': '2023:00:00', #wrong format
                'sleep_time': '23:00:00'}
               # 'interval': '60'}  #test missing one required parameter
        response = self.client.post(self.set_settings_url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Notification.objects.count(), 0)        
    

    def test_get_settings_success(self):
        """Test successfully retrieving user notification settings."""
        Notification.objects.create(user=self.user, 
                                    wakeup_time='07:00:00', 
                                    sleep_time='23:00:00', 
                                    interval=60)
        response = self.client.get(self.get_settings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data'], 
                         {'wakeup_time': '07:00:00', 
                          'sleep_time': '23:00:00', 
                          'interval': 60})

    def test_get_settings_not_found(self):
        """ Test response when user settings are not found."""
        response = self.client.get(self.get_settings_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(response.json()['message'], 'Settings not found')

