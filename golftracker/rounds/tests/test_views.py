import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User

from ..views import isOwnerOrPublic, isOwner, createRound
from ..models import Round, Score
from courselibrary.models import Course, Tee


class IsOwnerOrPublicHelperFunctionTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username='testuser', password='12345')
        User.objects.create(username='nonowner', password='12345')
        course = Course.objects.create(name='Cedarholm Golf Course',
                              location='Roseville, MN',
                              creator=user, num_of_holes="09")
        tee = Tee.objects.create(name='Red', course=course)
        Round.objects.create(player=user, course=course,
                                     tees=tee, num_of_holes='18')
        
    def test_is_owner(self):
        """Test the user is not the owner. Should return False"""
        non_owner_user = User.objects.get(username='nonowner')
        round = Round.objects.get(pk=1)
        result = isOwner(round, non_owner_user)
        self.assertFalse(result)

    def test_is_not_owner_but_is_public(self):
        """User is the owner. Should return True"""
        user = User.objects.get(username='testuser')
        round = Round.objects.get(pk=1)
        result = isOwner(round, user)
        self.assertTrue(result)


class IsOwnerHelperFunctionTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username='testuser', password='12345')
        User.objects.create(username='nonowner', password='12345')
        course = Course.objects.create(name='Cedarholm Golf Course',
                              location='Roseville, MN',
                              creator=user, num_of_holes="09")
        tee = Tee.objects.create(name='Red', course=course)
        Round.objects.create(player=user, course=course,
                                     tees=tee, num_of_holes='18')
        Round.objects.create(player=user, course=course,
                                     tees=tee, num_of_holes='18', public=True)
        
    def test_is_not_owner_and_is_not_public(self):
        """Round is not public and the user is not the owner. Should return False"""
        non_owner_user = User.objects.get(username='nonowner')
        round = Round.objects.get(pk=1)
        result = isOwnerOrPublic(round, non_owner_user)
        self.assertFalse(result)

    def test_is_not_owner_but_is_public(self):
        """Round is public and the user is not the owner. Should return True"""
        non_owner_user = User.objects.get(username='nonowner')
        round = Round.objects.get(pk=2)
        result = isOwnerOrPublic(round, non_owner_user)
        self.assertTrue(result)

    def test_is_owner_and_is_not_public(self):
        """Round is not public but the user is the owner. Should return True"""
        user = User.objects.get(username='testuser')
        round = Round.objects.get(pk=1)
        result = isOwnerOrPublic(round, user)
        self.assertTrue(result)

    def test_is_owner_and_is_public(self):
        """Round is public and the user is the owner. Should return True"""
        user = User.objects.get(username='testuser')
        round = Round.objects.get(pk=2)
        result = isOwnerOrPublic(round, user)
        self.assertTrue(result)


class CreateRoundTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username='testuser', password='12345')
        cedarholm = Course.objects.create(name='Cedarholm Golf Course',
                                       location='Roseville, MN',
                                       creator=user, num_of_holes="09")
        islandlake = Course.objects.create(name='Island Lake',
                                           location='Shoreview, MN',
                                           creator=user, num_of_holes="09")
        Tee.objects.create(name='White', course=cedarholm)
        Tee.objects.create(name='Blue', course=islandlake)

    def test_rejects_unloggedin_user(self):
        """Check that an unlogged in user is redirected"""
        client = Client()
        response = client.get('/roundslibrary/create/')
        self.assertEqual(response.status_code, 302)

    def test_renders_correct_template(self):
        """Check that the correct template is rendered"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        response = client.get('/roundslibrary/create/')
        self.assertTemplateUsed(response, 'rounds/create_round.html')

    def test_round_can_be_posted_successfully(self):
        """Check that a post with valid data can create a round successfully"""
        user = User.objects.get(username='testuser')
        course = Course.objects.get(name='Cedarholm Golf Course')
        tee = Tee.objects.get(name='White')
        client = Client()
        client.force_login(user)
        payload = {'course': '1',
                   'tees': '1',
                   'num_of_holes': 'F9'}
        client.post('/roundslibrary/create/', payload)
        round = Round.objects.get(pk=1)
        self.assertEqual(round.player, user)
        self.assertEqual(round.course, course)
        self.assertEqual(round.tees, tee)
        self.assertEqual(round.num_of_holes, 'F9')
        #Make sure datetime is automatically added, testing to ensure it is within +/- 1 day
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days = 1)
        tomorrow = today + datetime.timedelta(days = 1)
        self.assertTrue(round.datetime.date() <= tomorrow and round.datetime.date() >= yesterday)

    def test_round_with_invalid_data_is_not_posted(self):
        """Check that a post with invalid data is not created"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        payload = {'course': '1',
                   'tees': '1',
                   'num_of_holes': '00'}
        client.post('/roundslibrary/create/', payload)
        round = Round.objects.all()
        self.assertQuerySetEqual(round, Round.objects.none())

    def test_tee_associated_with_incorrect_course_doesnt_post(self):
        """Check that when a tee doens't coorespond to a the correct post
        object, the form is invalid"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        payload = {'course': '1',
                   'tees': '2',
                   'num_of_holes': 'F9'}
        client.post('/roundslibrary/create/', payload)
        round = Round.objects.all()
        self.assertQuerySetEqual(round, Round.objects.none())