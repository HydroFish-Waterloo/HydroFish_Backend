from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class UserAccountTests(APITestCase):
    
    def setUp(self):
        # This method is called before each test.
        self.register_url = reverse('api_register')  # Use the named URL for registration
        self.login_url = reverse('api_login')  # Use the named URL for login
        self.user_data = {
            'username': 'arthur',
            'password': '147258@@@'
        }
        self.user_data2 = { ## wrong data for registeration
            'username': 'arthur2',
            'password': '147258'
        }
        self.user_data21 = { ## wrong data for registeration
            'username': 'arthur3',
            'password': '14725800'
        }

        self.user_data3 = {
            'username': 'arthur',  ## wrong data for repeated user
            'password': '147258@@@@@@'
        }
        self.user_data4 = {  ## not registered user
            'username': 'arthur4',
            'password': '147258@@@'
        }        

        return super().setUp()

    def test_register_user(self):
        """
        Ensure we can create a new user and a valid token is returned.
        """
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)
        token_length = len(response.data['token'])
        self.assertTrue(token_length > 0)
        ## test for repeated user name
        response = self.client.post(self.register_url, self.user_data3, format='json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) ## should assert '400' error.


    def test_register_user2(self): ## error cases
        """
        Test register with weak passward/ repeated user.
        """
        response = self.client.post(self.register_url, self.user_data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) ## should assert '400' error.

        response = self.client.post(self.register_url, self.user_data21, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) ## should assert '400' error.



    def test_login_user(self):
        """
        Ensure we can log in a user and a valid token is returned.
        """
        self.client.post(self.register_url, self.user_data, format='json')  # Register user first
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        token_length = len(response.data['token'])
        self.assertTrue(token_length > 0)

    def test_login_invalid_user(self):
        """
        Ensure user cannot log in with incorrect credentials.
        """
        response = self.client.post(self.login_url, {'username': 'wrong', 'password': 'pass'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.login_url, self.user_data4, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 



        



