from django.utils import unittest
from django.test.client import Client
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
import time
import selenium.webdriver as webdriver



class Rendered_user(unittest.TestCase):


    def setUp(self):
        self.client = Client()


    def test_login(self):
        """test checks login_view  responses with login form"""
        request = Client()
        response = request.get('/')
        self.assertIn("form",response.context_data.keys())

    def test_logout(self):
        # redirects on logout
        request = Client()
        response = request.get('/accounts/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('testserver',response.get('Location'))


    def test_dashboard(self):
        """test checks the redirection of account/dashboard
        without loging in if the user enters acconuts/dashboard
        it redirects to login page"""
        request = Client()
        response = request.get('/accounts/dashboard/')
        self.assertIn('accounts/login/?next=/accounts/dashboard/',response.get('Location'))
