from django.test import TestCase
from django.contrib.auth.models import User
from random import randint

from ..models import Course, Tee, Hole

class CourseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        Course.objects.create(name='Cedarholm Golf Course',
                              location='Roseville, MN',
                              creator=self.user, num_of_holes="09")
        
    def test_course_string_representation(self):
        """Test to ensure that a Course object returns the correct string representation"""
        cedarholm = Course.objects.get(name='Cedarholm Golf Course')
        self.assertEqual(cedarholm.__str__(), 'Cedarholm Golf Course')


class TeeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        cedarholm = Course.objects.create(name='Cedarholm Golf Course',
                                        location='Roseville, MN',
                                        creator=self.user, num_of_holes="09")
        Tee.objects.create(name='Red', course=cedarholm)
        Tee.objects.create(name='White', course=cedarholm, course_rating=30.5, slope_rating=70.0)

    def test_tee_string_representation(self):
        """Test to ensure that a Tee object returns the correct string representation"""
        white = Tee.objects.get(name='White')
        self.assertEqual(white.__str__(), 'White')


class HoleTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        cedarholm = Course.objects.create(name='Cedarholm Golf Course',
                                        location='Roseville, MN',
                                        creator=self.user, num_of_holes="09")
        white_tees = Tee.objects.create(name='Red', course=cedarholm)
        for i in range(18):
            Hole.objects.create(number=i + 1, par=3, yards=randint(50, 300), tees=white_tees)

    def test_tee_string_representation(self):
        """Test to ensure that a Hole object returns the correct string representation"""
        hole_3 = Hole.objects.get(number='3')
        self.assertEqual(hole_3.__str__(), '3')


