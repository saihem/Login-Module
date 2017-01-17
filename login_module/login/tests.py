from django.test import TestCase
from django.test.client import Client
from django.test import LiveServerTestCase
from django.contrib.auth.models import User

class RenderedUser(TestCase):

    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(username="temporary", password="temporary")

    def test_login(self):
        """test checks login_view responses with login form"""
        request = Client()
        response = request.get('/')
        self.assertIn("form",response.context_data.keys())
        self.client.login(username='temporary', password='temporary')


    def test_logout(self):
        """test checks logout responses"""
        request = Client()
        response = request.get('/logout/')
        self.assertEqual(response.status_code, 302)

    def test_dashboard(self):
        """test checks the redirection of users/ to login page if user is
        not logged in"""
        request = Client()
        response = request.get('/users/')
        self.assertIn('/?next=/users/',response.get('Location'))
