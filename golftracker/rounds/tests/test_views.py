import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User

from ..views import isOwnerOrPublic, isOwner, createScoreCard
from ..models import Round, Score
from courselibrary.models import Course, Tee, Hole


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


class CreateScoreCardHelperFunctionTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username='testuser', password='12345')
        dwan = Course.objects.create(name='Dwan Golf Club',
                                       location='Bloomington, MN',
                                       creator=user, num_of_holes="18")
        tee = Tee.objects.create(name='Woods', course=dwan)
        for i in range(int(dwan.num_of_holes)):
            Hole.objects.create(number=i + 1, par=4, yards=(i + 1) * 10, tees=tee)
        Round.objects.create(player=user, course=dwan, tees=tee, num_of_holes='F9')
        Round.objects.create(player=user, course=dwan, tees=tee, num_of_holes='B9')
        Round.objects.create(player=user, course=dwan, tees=tee, num_of_holes='18')

    def test_front_nine_creates_scores_correctly(self):
        """Testing createScoreCard function with the selection set to front nine"""
        front_nine_round = Round.objects.get(num_of_holes='F9')
        tees = Tee.objects.get(pk=1)
        createScoreCard(front_nine_round, tees)
        scores = Score.objects.filter(round=front_nine_round)
        self.assertEqual(len(scores), 9)
        for i, score in enumerate(scores):
            self.assertEqual(score.hole_number, i + 1)
            self.assertEqual(score.yardage, (i + 1) * 10)
            self.assertEqual(score.par, 4)
            self.assertFalse(score.score)

    def test_front_nine_creates_scores_correctly(self):
        """Testing createScoreCard function with the selection set to back nine"""
        back_nine_round = Round.objects.get(num_of_holes='B9')
        tees = Tee.objects.get(pk=1)
        createScoreCard(back_nine_round, tees)
        scores = Score.objects.filter(round=back_nine_round)
        self.assertEqual(len(scores), 9)
        for i, score in enumerate(scores):
            self.assertEqual(score.hole_number, (i + 9) + 1)
            self.assertEqual(score.yardage, ((i + 9) + 1) * 10)
            self.assertEqual(score.par, 4)
            self.assertFalse(score.score)

    def test_eighteen_creates_scores_correctly(self):
        """Testing createScoreCard function with the selection set to eighteen holes"""
        eighteen_round = Round.objects.get(num_of_holes='18')
        tees = Tee.objects.get(pk=1)
        createScoreCard(eighteen_round, tees)
        scores = Score.objects.filter(round=eighteen_round)
        self.assertEqual(len(scores), 18)
        for i, score in enumerate(scores):
            self.assertEqual(score.hole_number, i + 1)
            self.assertEqual(score.yardage, (i + 1) * 10)
            self.assertEqual(score.par, 4)
            self.assertFalse(score.score)


class CreateRoundTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username='testuser', password='12345')
        cedarholm = Course.objects.create(name='Cedarholm Golf Course',
                                       location='Roseville, MN',
                                       creator=user, num_of_holes="09")
        islandlake = Course.objects.create(name='Island Lake',
                                           location='Shoreview, MN',
                                           creator=user, num_of_holes="09")
        white_tee = Tee.objects.create(name='White', course=cedarholm)
        Tee.objects.create(name='Blue', course=islandlake)
        for i in range(int(cedarholm.num_of_holes)):
            Hole.objects.create(number=i + 1, par=3, yards=(i + 1) * 10, tees=white_tee)

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

    def test_scorecard_creation_if_round_is_posted_successfully(self):
        """When a round is created an associated scorecard should be created as
        well, for modularity a seperate function is being called to handle that
        which will have seperate tests. Here we are testing that all of the data is
        passed to that correctly and the expected objects are created."""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        payload = {'course': '1',
                   'tees': '1',
                   'num_of_holes': 'F9'}
        client.post('/roundslibrary/create/', payload)
        round = Round.objects.get(pk=1)
        scores = Score.objects.filter(round=round).order_by('hole_number')
        self.assertEqual(len(scores), 9)
        for i, score in enumerate(scores):
            self.assertEqual(score.hole_number, i + 1)
            self.assertEqual(score.yardage, (i + 1) * 10)
            self.assertEqual(score.par, 3)
            self.assertFalse(score.score)
        