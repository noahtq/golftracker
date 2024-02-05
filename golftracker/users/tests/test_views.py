import os
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user

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
        an associated profile object, also tests signals.py"""
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


class ProfileViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser', password='12345')

    def test_renders_correct_template(self):
        """Check that the correct template is rendered"""
        client = Client()
        client.force_login(self.user)
        response = client.get('/profile/')
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_rejects_unloggedin_user(self):
        """Check that an unlogged in user is redirected"""
        client = Client()
        response = client.get('/profile/')
        self.assertEqual(response.status_code, 302)
        
    def test_successful_post_updates_user_and_profile_correctly(self):
        """Checking that a successful post updates the correct info
        in the user and profile object"""
        client = Client()
        client.force_login(self.user)
        image_path = './users/tests/test_media/test_profile_photo.jpeg'
        image = SimpleUploadedFile(name='test_profile_photo_compressed.jpeg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        payload = {'username': 'testuser1',
                   'email': 'testuser1@gmail.com',
                   'image': image}
        client.post('/profile/', payload)
        updated_user = User.objects.get(pk=1)
        updated_profile = Profile.objects.get(pk=1)
        self.assertEqual(updated_user.username, 'testuser1')
        self.assertEqual(updated_user.email, 'testuser1@gmail.com')
        self.assertEqual(updated_profile.image, 'profile_pics/test_profile_photo_compressed.jpeg')
        #Delete test image from media folder once we are done with test
        saved_image_path = os.path.join(os.getcwd(), 'media/profile_pics/test_profile_photo_compressed.jpeg')
        os.remove(saved_image_path)

    def test_successful_post_updates_user_and_profile_correctly(self):
        """Checking that a successful post redirects to correct url"""
        client = Client()
        client.force_login(self.user)
        image_path = './users/tests/test_media/test_profile_photo.jpeg'
        image = SimpleUploadedFile(name='test_profile_photo_compressed.jpeg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        payload = {'username': 'testuser1',
                   'email': 'testuser1@gmail.com',
                   'image': image}
        response = client.post('/profile/', payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/profile/')
        #Delete test image from media folder once we are done with test
        saved_image_path = os.path.join(os.getcwd(), 'media/profile_pics/test_profile_photo_compressed.jpeg')
        os.remove(saved_image_path)


#Django Default View so code coverage for this test case only found in golftracker/urls.py
class LoginViewTestCase(TestCase):
    def test_renders_correct_template(self):
        """Check that the correct template is rendered"""
        client = Client()
        response = client.get('/login/')
        self.assertTemplateUsed(response, 'users/login.html')


class LogoutViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='username', password='12345')
    
    def test_renders_correct_template(self):
        """Check that the correct template is rendered"""
        client = Client()
        client.force_login(self.user)
        response = client.post('/logout/')
        self.assertTemplateUsed(response, 'users/logout.html')