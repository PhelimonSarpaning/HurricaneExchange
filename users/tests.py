from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import SESSION_KEY
from django.test import TestCase, override_settings
from users.forms import userEmailForm
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')


class MyTestCase(TestCase):
    def setUp(self):
        self.form_data = {
            'username':'Test',
            'email':'email@test.com',
            'password1':'SecretPass123',
            'password2':'SecretPass123'
        }


class userTests(MyTestCase):

    def test_RegistrationForm(self):
        form = userEmailForm(data=self.form_data)
        self.assertTrue(form.is_valid())
    
