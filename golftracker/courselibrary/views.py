from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import PermissionDenied

from .models import Course


#Only allow user to make changes to a course if they
#   1. Created the course and the course isn't verified
#   2. Are a staff member
def canEditCourse(request, course):
    creator = course.creator
    user = request.user
    is_staff = request.user.is_staff
    if course.verified:
        return is_staff
    else:
        return creator == user or is_staff
    

def courseList(request):
    courses = Course.objects.all()
    context = {"courses": courses}
    return render(request, 'courselibrary/courselibrary.html', context)


def courseDetails(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    return render(request, 'courselibrary/detail.html', {'course': course})


def courseEdit(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    if canEditCourse(request, course) == False:
        raise PermissionDenied()
    return render(request, 'courselibrary/edit.html', {'course': course})