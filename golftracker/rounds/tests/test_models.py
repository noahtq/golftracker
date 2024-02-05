from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Round, Score
from courselibrary.models import Course, Tee


class RoundModelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser', password='12345')
        course = Course.objects.create(name='Cedarholm Golf Course',
                              location='Roseville, MN',
                              creator=self.user, num_of_holes="09")
        tee = Tee.objects.create(name='Red', course=course)
        Round.objects.create(player=self.user, course=course,
                                     tees=tee, num_of_holes='18')

    def test_can_create_object_with_default_values(self):
        """Checking to make sure a rounds object can be created
        with the expected values being left as default, also
        doubles as a test to make sure object can be created
        successfully"""
        course = Course.objects.get(pk=1)
        tee = Tee.objects.get(pk=1)
        round = Round.objects.create(player=self.user, course=course,
                                     tees=tee, num_of_holes='18')
        self.assertTrue(round)

    def test_correct_str_representation_for_model(self):
        """Test to ensure that a Round object returns the correct string representation"""
        round = Round.objects.get(pk=1)
        self.assertEqual(round.__str__(), 'Cedarholm Golf Course, Round ID: 1')


class ScoreModelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser', password='12345')
        course = Course.objects.create(name='Cedarholm Golf Course',
                              location='Roseville, MN',
                              creator=self.user, num_of_holes="09")
        tee = Tee.objects.create(name='Red', course=course)
        round = Round.objects.create(player=self.user, course=course,
                                     tees=tee, num_of_holes='18')
        Score.objects.create(round=round, hole_number=3, par=3, yardage=100, score=5)

    def test_correct_str_representation_for_model(self):
        """Test to ensure that a Score object returns the correct string representation"""
        score = Score.objects.get(pk=1)
        self.assertEqual(score.__str__(), 'Cedarholm Golf Course, Round ID: 1, Hole: 3')