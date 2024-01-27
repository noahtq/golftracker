from django.test import TestCase, Client
from django.contrib.auth.models import User

from ..models import Course
from ..views import canEditCourse, courseList


class CanEditCourseHelperFunctionTestCase(TestCase):
    def setUp(self):
        regular_user = User.objects.create_user(username='testuser', password='12345')
        User.objects.create_user(username='testuser2', password='12345')
        staff_user = User.objects.create_user(username='staffuser', password='12345', is_staff=True)
        #Non verified course, User owned
        Course.objects.create(name='Cedarholm Golf Course',
                        location='Roseville, MN',
                        creator=regular_user, num_of_holes="09")
        #Non Verified course, Staff Owned
        Course.objects.create(name='Island Lake Golf Course',
                        location='Arden Hills, MN',
                        creator=staff_user, num_of_holes="09")
        #Verified course, User owned
        Course.objects.create(name='Dwan Golf Course',
                        location='Bloomington, MN',
                        creator=regular_user, num_of_holes="18", verified=True)
        #Verified course, Staff owned
        Course.objects.create(name='Edinburgh USA',
                        location='Brooklyn Park, MN',
                        creator=staff_user, num_of_holes="18", verified=True)
        
    def test_non_staff_user_and_not_creator_course_not_verified(self):
        """Test canEditCourse() helper function returns False when
        the user is neither staff nor the course creator. Course is
        not verified"""
        course = Course.objects.get(name='Cedarholm Golf Course')
        user = User.objects.get(username='testuser2')
        self.assertFalse(canEditCourse(user, course))

    def test_non_staff_user_but_is_creator_course_not_verified(self):
        """Test canEditCourse() helper function returns True when
        the user is not staff but is the course creator. Course is
        not verified"""
        course = Course.objects.get(name='Cedarholm Golf Course')
        user = User.objects.get(username='testuser')
        self.assertTrue(canEditCourse(user, course))

    def test_staff_user_but_is_not_creator_course_not_verified(self):
        """Test canEditCourse() helper function returns True when
        the user is staff but is not the course creator. Course is
        not verified"""
        course = Course.objects.get(name='Cedarholm Golf Course')
        user = User.objects.get(username='staffuser')
        self.assertTrue(canEditCourse(user, course))

    def test_staff_user_and_is_creator_course_not_verified(self):
        """Test canEditCourse() helper function returns True when
        the user is staff and is the course creator. Course is
        not verified"""
        course = Course.objects.get(name='Island Lake Golf Course')
        user = User.objects.get(username='staffuser')
        self.assertTrue(canEditCourse(user, course))

    def test_non_staff_user_and_not_creator_course_verified(self):
        """Test canEditCourse() helper function returns False when
        the user is not staff and is not the course creator. Course is
        verified"""
        course = Course.objects.get(name='Dwan Golf Course')
        user = User.objects.get(username='testuser2')
        self.assertFalse(canEditCourse(user, course))

    def test_non_staff_user_but_is_creator_course_verified(self):
        """Test canEditCourse() helper function returns False when
        the user is not staff but is the course creator. Course is
        verified"""
        course = Course.objects.get(name='Dwan Golf Course')
        user = User.objects.get(username='testuser')
        self.assertFalse(canEditCourse(user, course))

    def test_staff_user_but_is_not_creator_course_verified(self):
        """Test canEditCourse() helper function returns True when
        the user is staff but is not the course creator. Course is
        verified"""
        course = Course.objects.get(name='Dwan Golf Course')
        user = User.objects.get(username='staffuser')
        self.assertTrue(canEditCourse(user, course))

    def test_staff_user_and_is_creator_course_verified(self):
        """Test canEditCourse() helper function returns True when
        the user is staff and is the course creator. Course is
        verified"""
        course = Course.objects.get(name='Edinburgh USA')
        user = User.objects.get(username='staffuser')
        self.assertTrue(canEditCourse(user, course))


class CourseListViewTestCase(TestCase):
    def setUp(self) -> None:
        regular_user = User.objects.create_user(username='testuser', password='12345')
        Course.objects.create(name='Cedarholm Golf Course',
                        location='Roseville, MN',
                        creator=regular_user, num_of_holes="09")
        Course.objects.create(name='Island Lake Golf Course',
                        location='Arden Hills, MN',
                        creator=regular_user, num_of_holes="09")
        
    def test_rejects_unloggedin_user(self):
        """Check that an unlogged in user is redirected"""
        client = Client()
        response = client.get('/courselibrary/')
        self.assertEqual(response.status_code, 302)
        
    def test_returns_all_courses(self):
        """Check that a list of all of the courses is returned as context data"""
        courses = Course.objects.all()

        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        response = client.get('/courselibrary/')
        response_courses = response.context['courses']

        self.assertQuerysetEqual(response_courses, courses, ordered=False)

    def test_renders_correct_template(self):
        """Check that the correct template is rendered"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        response = client.get('/courselibrary/')
        self.assertTemplateUsed(response, 'courselibrary/courselibrary.html')