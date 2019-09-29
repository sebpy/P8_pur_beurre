from django.urls import reverse
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User

from library.forms import LoginForm, RegisterForm


class IndexPageTestCase(TestCase):
    """ Test index page """
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class LegalPageTestCase(TestCase):
    """ Test index page """
    def test_legal_page(self):
        response = self.client.get(reverse('legal_notice'))
        self.assertEqual(response.status_code, 200)


class TestLoginFormTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User.objects.create_user(username="Test",
                                 email="test@django.fr",
                                 password="testdjango")

        self.user = User.objects.get(username='Test')

    def test_valid_form(self):
        username = self.user.username
        password = self.user.password
        data = {'username': username, 'password': password, }
        form = LoginForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'username': '', 'password': '', }
        form = LoginForm(data=data)
        self.assertFalse(form.is_valid())


class TestRegisterFormTestCase(TestCase):

    def test_valid_form(self):
        user_register = User.objects.create_user(username="Test",
                                                 email="test@django.fr",
                                                 password="testdjango")
        data = {'username': user_register.username, 'email': user_register.email, 'password1': user_register.password,
                'password2': user_register.password, }
        form = RegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        user_register = User.objects.create_user(username="Test",
                                                 email="test@django.fr",
                                                 password="")
        data = {'username': user_register.username, 'email': user_register.email, 'password': user_register.password, }
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())
