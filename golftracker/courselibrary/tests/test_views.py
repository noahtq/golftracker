import re
import json
from random import randint
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.forms import modelformset_factory

from ..models import Course, Tee, Hole
from ..views import canEditCourse
from ..forms import CourseCreateForm, CourseUpdateForm, TeeCreateForm


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


class CourseCreateTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create(username='testuser', password='12345')

    def test_rejects_unloggedin_user(self):
        """Check that an unlogged in user is redirected"""
        client = Client()
        response = client.get('/courselibrary/create/')
        self.assertEqual(response.status_code, 302)

    def test_renders_correct_template(self):
        """Check that the correct template is rendered"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        response = client.get('/courselibrary/create/')
        self.assertTemplateUsed(response, 'courselibrary/create.html')

    def test_sends_form_as_context(self):
        """Check that the view passes the correct form as context"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        response = client.get('/courselibrary/create/')
        self.assertEquals(type(response.context["form"]), CourseCreateForm)

    def test_posts_creates_course_correctly(self):
        """Check that the view when posted creates the course object correctly"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        client.post('/courselibrary/create/', {'name': 'Island Lake Golf Course',
                                                        'location': 'Arden Hills, MN',
                                                        'num_of_holes': '09'})
        course = Course.objects.get(name='Island Lake Golf Course')
        self.assertEqual(course.name, "Island Lake Golf Course")
        self.assertEqual(course.location, "Arden Hills, MN")
        self.assertEqual(course.num_of_holes, "09")
        self.assertEqual(course.creator, user)

    def test_does_not_create_course_when_data_incorrect(self):
        """Check that the view does not post when passed incorrect data"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        client.post('/courselibrary/create/', {'name': 'Island Lake Golf Course',
                                                        'location': 'Arden Hills, MN',
                                                        'num_of_holes': '15'})
        course = Course.objects.filter(name='Island Lake Golf Course')
        self.assertQuerySetEqual(course, Course.objects.none())

    def test_that_successful_post_redirects(self):
        """Check that a successful post redirects users to correct url"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        response = client.post('/courselibrary/create/', {'name': 'Island Lake Golf Course',
                                                        'location': 'Arden Hills, MN',
                                                        'num_of_holes': '09'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/courselibrary/1/edit/')


class CourseDetailsViewTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username='testuser', password='12345')
        Course.objects.create(name='Cedarholm Golf Course',
                location='Roseville, MN',
                creator=user, num_of_holes="09")
        
    def test_rejects_unloggedin_user(self):
        """Check that an unlogged in user is redirected"""
        client = Client()
        response = client.get('/courselibrary/1/')
        self.assertEqual(response.status_code, 302)

    def test_renders_correct_template(self):
        """Check that the correct template is rendered"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        response = client.get('/courselibrary/1/')
        self.assertTemplateUsed(response, 'courselibrary/detail.html')

    def test_raises_404_if_course_does_not_exist(self):
        """Check that 404 is thrown if the course doesn't exist"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        response = client.get('/courselibrary/5/')
        self.assertEqual(response.status_code, 404)

    def test_passes_correct_course_as_context(self):
        user = User.objects.get(username='testuser')
        course = Course.objects.get(pk=1)
        client = Client()
        client.force_login(user)
        response = client.get('/courselibrary/1/')
        self.assertEqual(response.context["course"], course)


class CourseEditViewTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username='testuser', password='12345')
        course = Course.objects.create(name='Cedarholm Golf Course',
                location='Roseville, MN',
                creator=user, num_of_holes="09")
        Tee.objects.create(name='White', course=course)
        Tee.objects.create(name='Red', course=course)

    def test_rejects_unloggedin_user(self):
        """Check that an unlogged in user is redirected"""
        client = Client()
        response = client.get('/courselibrary/1/edit/')
        self.assertEqual(response.status_code, 302)

    def test_renders_correct_template(self):
        """Check that the correct template is rendered"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        response = client.get('/courselibrary/1/edit/')
        self.assertTemplateUsed(response, 'courselibrary/edit.html')

    def test_raises_404_if_course_does_not_exist(self):
        """Check that 404 is thrown if the course doesn't exist"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        response = client.get('/courselibrary/5/edit/')
        self.assertEqual(response.status_code, 404)

    def test_that_permission_denied_if_cant_edit_course(self):
        """Check that permission is denied if user does not have permission 
        to edit course per the canEditCourse() function"""
        user = User.objects.create(username='wronguser', password='12345')
        client = Client()
        client.force_login(user)
        response = client.get('/courselibrary/1/edit/')
        self.assertEqual(response.status_code, 403)

    def test_that_correct_context_is_passed(self):
        """Check that the correct information is passed into the context data"""
        user = User.objects.get(username='testuser')
        course = Course.objects.get(name='Cedarholm Golf Course')
        tees = Tee.objects.filter(course=course)
        client = Client()
        client.force_login(user)
        response = client.get('/courselibrary/1/edit/')
        self.assertEqual(response.context['course'], course)
        self.assertEqual(type(response.context['form']), CourseUpdateForm)
        self.assertQuerySetEqual(response.context['tees'], tees, ordered=False)

    def test_course_is_altered_when_post_successful(self):
        """Check that the course is edited correctly when user submits
        correct data"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        client.post('/courselibrary/1/edit/', {'name': 'Island Lake Golf Course',
                                                         'location': 'Arden Hills, MN',
                                                         'num_of_holes': '18'})
        course = Course.objects.get(pk=1)
        self.assertEqual(course.name, "Island Lake Golf Course")
        self.assertEqual(course.location, "Arden Hills, MN")
        self.assertEqual(course.num_of_holes, "18")

    def test_course_is_not_altered_when_data_incorrect(self):
        """Check that the course is not edited correctly when user submits
        bad data"""
        original_course = Course.objects.get(pk=1)
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        client.post('/courselibrary/1/edit/', {'name': 'Island Lake Golf Course',
                                                         'location': 'Arden Hills, MN',
                                                         'num_of_holes': '52'})
        course = Course.objects.get(pk=1)
        self.assertEqual(original_course, course)

    def test_successful_post_redirects_to_correct_url(self):
        """Check that a successful posts redirects to the correct url"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        response = client.post('/courselibrary/1/edit/', {'name': 'Island Lake Golf Course',
                                                         'location': 'Arden Hills, MN',
                                                         'num_of_holes': '18'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/courselibrary/1/')


class CourseDeleteViewTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username='testuser', password='12345')
        course = Course.objects.create(name='Cedarholm Golf Course',
                location='Roseville, MN',
                creator=user, num_of_holes="09")
        Tee.objects.create(name='White', course=course)
        Tee.objects.create(name='Red', course=course)

    def test_rejects_unloggedin_user(self):
        """Check that an unlogged in user is redirected"""
        client = Client()
        response = client.get('/courselibrary/1/delete/')
        self.assertEqual(response.status_code, 302)

    def test_renders_correct_template(self):
        """Check that the correct template is rendered"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        response = client.get('/courselibrary/1/delete/')
        self.assertTemplateUsed(response, 'courselibrary/confirm_course_delete.html')

    def test_raises_404_if_course_does_not_exist(self):
        """Check that 404 is thrown if the course doesn't exist"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        response = client.get('/courselibrary/5/delete/')
        self.assertEqual(response.status_code, 404)

    def test_that_permission_denied_if_cant_edit_course(self):
        """Check that permission is denied if user does not have permission 
        to edit course per the canEditCourse() function"""
        user = User.objects.create(username='wronguser', password='12345')
        client = Client()
        client.force_login(user)
        response = client.get('/courselibrary/1/delete/')
        self.assertEqual(response.status_code, 403)

    def test_that_course_and_tees_deleted_if_post_is_successful(self):
        """Check that if the user posts the form, that the course is deleted
        from the database and the associated tees are deleted as well"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        client.post('/courselibrary/1/delete/')
        courses = Course.objects.all()
        tees = Tee.objects.all()
        self.assertQuerySetEqual(courses, Course.objects.none())
        self.assertQuerySetEqual(tees, Tee.objects.none())


class TeeCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username='testuser', password='12345')
        course = Course.objects.create(name='Cedarholm Golf Course',
                location='Roseville, MN',
                creator=user, num_of_holes="09")
        
    def test_rejects_unloggedin_user(self):
        """Check that an unlogged in user is redirected"""
        client = Client()
        response = client.get('/courselibrary/1/newtee/')
        self.assertEqual(response.status_code, 302)

    def test_renders_correct_template(self):
        """Check that the correct template is rendered"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        response = client.get('/courselibrary/1/newtee/')
        self.assertTemplateUsed(response, 'courselibrary/tee_create.html')

    def test_raises_404_if_course_does_not_exist(self):
        """Check that 404 is thrown if the course doesn't exist"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        response = client.get('/courselibrary/5/newtee/')
        self.assertEqual(response.status_code, 404)

    def test_that_permission_denied_if_cant_edit_course(self):
        """Check that permission is denied if user does not have permission 
        to edit course per the canEditCourse() function"""
        user = User.objects.create(username='wronguser', password='12345')
        client = Client()
        client.force_login(user)
        response = client.get('/courselibrary/1/newtee/')
        self.assertEqual(response.status_code, 403)

    def test_that_correct_context_is_passed(self):
        """Check that the correct information is passed into the context data"""
        user = User.objects.get(username='testuser')
        course = Course.objects.get(name='Cedarholm Golf Course')
        client = Client()
        client.force_login(user)
        response = client.get('/courselibrary/1/newtee/')
        self.assertEqual(type(response.context['form']), TeeCreateForm)
        '''Fix this so that we are testing all of the correct context is passed'''
        self.assertTrue(response.context['hole_formset'])
        self.assertEqual(response.context['course'], course)

    def test_that_correct_number_of_hole_fields_are_given(self):
        """Check that the correct number of fields for holes are given based on
        the courses number of holes"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        response = client.get('/courselibrary/1/newtee/')
        matches = re.findall(r'<input type="hidden" name="form-\d-id" id="id_form-\d-id"',
                   str(response.context['hole_formset']))
        self.assertEqual(len(matches), 9)

    def test_successful_post_creates_objects_correctly(self):
        """Check that a successful post makes our tee and hole objects correctly
        in the database"""
        user = User.objects.get(username='testuser')
        course = Course.objects.get(name='Cedarholm Golf Course')
        client = Client()
        client.force_login(user)
        payload = {'name': 'White', 'course_rating': '24.8', 'slope_rating': '69.0',
                   'form-TOTAL_FORMS': '9', 'form-INITIAL_FORMS': '0'}
        for i in range(9):
            payload[f'form-{i}-par'] = '3'
            payload[f'form-{i}-yards'] = str((i + 1) * 10)
        client.post('/courselibrary/1/newtee/', payload)
        tee = Tee.objects.get(course=course)
        holes = Hole.objects.filter(tees=tee)
        self.assertEqual(tee.name, 'White')
        self.assertEqual(tee.course_rating, 24.8)
        self.assertEqual(tee.slope_rating, 69.0)
        for i, hole in enumerate(holes):
            self.assertEqual(hole.number, i + 1)
            self.assertEqual(hole.par, 3)
            self.assertEqual(hole.yards, (i + 1) * 10)


    def test_successful_post_redirects_to_correct_url(self):
        """Check that a successful post redirects to the correct url"""
        user = User.objects.get(username='testuser')
        client = Client()
        client.force_login(user)
        payload = {'name': 'White', 'course_rating': '24.8', 'slope_rating': '69.0',
                   'form-TOTAL_FORMS': '9', 'form-INITIAL_FORMS': '0'}
        for i in range(9):
            payload[f'form-{i}-par'] = '3'
            payload[f'form-{i}-yards'] = str((i + 1) * 10)
        response = client.post('/courselibrary/1/newtee/', payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/courselibrary/1/edit/')


class teeEditViewTestCase(TestCase):
    def setUp(self) -> None:
        return super().setUp()



        
        
    
    