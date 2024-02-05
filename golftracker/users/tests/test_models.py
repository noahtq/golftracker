import os
from PIL import Image
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Profile


class ProfileModelTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create(username='testuser', password='12345')

    def test_correct_str_representation(self):
        """Checking that a profile returns the correct str representation
        Also doubles to check that a profile can be created successfully"""
        profile = Profile.objects.get(pk=1)
        self.assertEqual(profile.__str__(), 'testuser Profile')

    def test_correct_default_image_is_used(self):
        """Checking that a user created with no profile image specified
        gets the correct default image"""
        profile = Profile.objects.get(pk=1)
        self.assertEqual(profile.image, 'default.png')

    def test_new_profile_image_is_saved_correctly(self):
        """Checking that a user can upload their own profile image and that it
        is saved in the correect resolution"""
        profile = Profile.objects.get(pk=1)
        image_path = './users/tests/test_media/test_profile_photo.jpeg'
        profile.image = SimpleUploadedFile(name='test_profile_photo_compressed.jpeg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        profile.save()
        img = Image.open(profile.image)
        self.assertTrue(img.width <= 300)
        self.assertTrue(img.height <= 300)
        #Delete test image from media folder once we are done with test
        saved_image_path = os.path.join(os.getcwd(), 'media/profile_pics/test_profile_photo_compressed.jpeg')
        os.remove(saved_image_path)

    def test_profile_is_deleted_when_user_deleted(self):
        """Checking that our profile is deleted when the associated user
        is deleted"""
        user = User.objects.get(username='testuser')
        user.delete()
        profile = Profile.objects.filter(pk=1)
        self.assertQuerySetEqual(profile, Profile.objects.none())
