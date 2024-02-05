from django.test import TestCase, Client
from django.contrib.auth.models import User

from ..models import Profile
from ..views import register, profile


class RegisterViewTestCase(TestCase):
    def test_renders_correct_template(self):
        """Check that the correct template is rendered"""
        client = Client()
        response = client.get('/register/')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_that_successful_post_redirects_to_correct_url(self):
        """Check that the user is redirected to the correct url after
        the user is successfully registered"""
        client = Client()
        payload = {'username': 'testuser',
                   'email': 'testuser@gmail.com',
                   'password1': 'testing321',
                   'password2': 'testing321'}
        response = client.post('/register/', payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')

    def test_that_successful_post_creates_user_and_profile(self):
        """Check that a successful post creates a user and creates
        an associated profile object"""
        client = Client()
        payload = {'username': 'testuser',
                   'email': 'testuser@gmail.com',
                   'password1': 'testing321',
                   'password2': 'testing321'}
        client.post('/register/', payload)
        user = User.objects.get(username='testuser')
        profile = Profile.objects.get(user=user)
        self.assertTrue(user)
        self.assertTrue(profile)

    def test_that_unsuccessful_post_doesnt_create_anything(self):
        """Check that an unsuccessful post doesn't create anything"""
        client = Client()
        payload = {'username': 'testuser',
                   'email': 'testuser@gmail.com',
                   'password2': 'testing321'}
        client.post('/register/', payload)
        user = User.objects.all()
        profile = Profile.objects.all()
        self.assertQuerySetEqual(user, User.objects.none())
        self.assertQuerySetEqual(profile, Profile.objects.none())