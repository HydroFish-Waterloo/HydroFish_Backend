from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class UserAccountTests(APITestCase):
    
    def setUp(self):
        # This method is called before each test.
        # Create a user for testing login
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.token = Token.objects.create(user=self.user)
        self.register_url = reverse('api_register')  # Use the named URL for registration
        self.login_url = reverse('api_login')  # Use the named URL for login      

        return super().setUp()
    
## this test will test login success/failure, register success/failure
## mainly test the failure cases
## login failure : error key, error value, key-value not matched
    def test_login_success(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_login_failure(self):
        """### test wrong password """
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """### test wrong key """
        data = {
            'username1': 'testuser', #error key
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """### test wrong key """
        data = {
            'username': 'testuser',
            'password1': 'testpassword123' #error key
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """### test wrong value, non-existing user """
        data = {
            'username': 'testuser_not_existing', #wrong user
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """### test missing all parameters  """
        data = " " #missing all
        response = self.client.post(self.login_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """### test missing 1st param """
        data = {
            'password': 'testpassword123' #missing 1st
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """### test missing 2nd param  """
        data = {
            'username': 'testuser',  #missing 2nd
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """### test missing 1st partly  """
        data = {
            'username': '', 
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """### test missing 2nd partly """
        data = {
            'username': 'testuser', 
            'password': ''
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """### test have extra data """
        data = {
            'username': 'testuser', 
            'password': 'testpassword123',
            'password': 'testpassword123455'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """### test have extra data, password """
        data = {
            'username': 'testuser', 
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """### test have extra data3 """
        data = {
            'username': 'testuser', 
            'password': 'testpassword123',
            'password1': 'testpassword123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



# Test register function
## register failure: weak password, unaccepatable password, not-matched password, duplicated user
        # self.assertTrue('token' in response.data)
        # token_length = len(response.data['token'])
        # self.assertTrue(token_length > 0)
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 

    def test_register_success(self):
        data = {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_register_failure(self):
        """ test duplicated user"""
        data = {
            'username': 'testuser',  # Assuming unique usernames are required, this should fail.
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """ test duplicated user2 """
        data = {
            'username': 'testuser',  # Assuming unique usernames are required, this should fail.
            'password': 'testpassword123',
            'password': 'testpassword123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """ test weak password1 '123' """
        data = {
            'username': 'testuser', 
            'password1': '12345678',
            'password2': '12345678'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """ test weak password2 'abc'"""
        data = {
            'username': 'testuser', 
            'password1': 'abcdef',
            'password2': 'abcdef'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """ test weak password3"""
        data = {
            'username': 'testuser', 
            'password1': '@@@@@@@@',
            'password2': '@@@@@@@@'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'username': 'testuser', 
            'password1': 'password',
            'password2': 'password'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """ test weak password4"""
        data = {
            'username': 'testuser', 
            'password1': 'ABCDEF',
            'password2': 'ABCDEF'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """ test weak password5"""
        data = {
            'username': 'testuser', 
            'password1': 'A',
            'password2': 'A'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """test unaccepatable password"""
        data = {
            'username': 'testuser', 
            'password1': '',
            'password2': ''
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)    

        data = {
            'username': 'testuser', 
            'password1': '_',
            'password2': '_'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)     

        data = {
            'username': 'testuser', 
            'password1': 'A',
            'password2': 'A'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)          

        data = {
            'username': 'testuser', 
            'password1': '@#$%^&*()',
            'password2': '@#$%^&*()'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)     

        """test not matched password"""
        data = {
            'username': 'testuser', 
            'password1': 'wrong12345',
            'password2': 'wrong12346'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'username': 'testuser', 
            'password1': 'wrong12345',
            'password2': 'wrong12345 '
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)       

        data = {
            'username': 'testuser', 
            'password1': ' wrong12345',
            'password2': 'wrong12345'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 

        data = {
            'username': 'testuser', 
            'password1': 'Wrong12345',
            'password2': 'wrong12345'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 

        data = {
            'username': 'testuser', 
            'password1': 'WRONG12345',
            'password2': 'wrong12345'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 

        """test invalid input"""
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 

        data = {
            'password1': 'wrong12345',#missing one
            'password2': 'wrong12345'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)         

        data = {
            'username': 'testuser', 
            'password2': 'wrong12345'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  

        data = {
            'username': 'testuser', 
            'password1': 'wrong12345',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)     

        data = {
            'username': 'testuser', 
            'password1': 'wrong12345',
            'password2': 'wrong12345',
            'password3': 'wrong12345' #extra one
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)       

        data = {
            'username': 'testuser', 
            'password': 'wrong12345', #error key
            'password': 'wrong12345'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)     

        data = {
            'usename': 'testuser',  #error key
            'password1': 'wrong12345',
            'password2': 'wrong12345'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)       

        data = {
            'username': 'testuser', 
            'password': 'wrong12345',
            'password1': 'wrong12345'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)       

        data = {
            'username': 'testuser', 
            'password1': 'wrong12345',
            'password2': 'wrong12345',
            'level' :  12 #extra data
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)                              
