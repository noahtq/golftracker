from django.shortcuts import render, redirect
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Tee, Hole
from .forms import CourseUpdateForm, TeeUpdateForm, HoleUpdateForm


#Only allow user to make changes to a course if they
#   1. Created the course and the course isn't verified
#   2. Are a staff member
def canEditCourse(request, course) -> bool:
    creator = course.creator
    user = request.user
    is_staff = request.user.is_staff
    if course.verified:
        return is_staff
    else:
        return creator == user or is_staff
    

@login_required
def courseList(request):
    courses = Course.objects.all()
    context = {"courses": courses}
    return render(request, 'courselibrary/courselibrary.html', context)


@login_required
def courseDetails(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    return render(request, 'courselibrary/detail.html', {'course': course})


@login_required
def courseEdit(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        tees = Tee.objects.filter(course=course)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    except Tee.DoesNotExist:
        raise Http404("Tees don't exist")
    if canEditCourse(request, course) == False:
        raise PermissionDenied()

    if request.method == 'POST':
        c_form = CourseUpdateForm(request.POST, instance=course)
        t_forms = []
        for tee in tees:
            t_forms.append(TeeUpdateForm(request.POST, instance=tee))
        t_forms_valid = True
        for form in t_forms:
            if form.is_valid() == False:
                t_forms_valid == False
        if c_form.is_valid() and t_forms_valid:
            c_form.save()
            for form in t_forms:
                form.save()
            messages.success(request, f'Course successfully update.')
            return redirect('courselibrary:courselibrary')
    else:
        c_form = CourseUpdateForm(instance=course)
        t_forms = []
        for tee in tees:
            t_forms.append(TeeUpdateForm(instance=tee))

    context = {
        'course': course,
        'c_form': c_form,
        't_forms': t_forms
    }


    return render(request, 'courselibrary/edit.html', context)