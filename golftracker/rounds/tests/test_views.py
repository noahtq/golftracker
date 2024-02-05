from django.test import TestCase
from django.contrib.auth.models import User

from ..views import isOwnerOrPublic, isOwner
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