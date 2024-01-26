from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory

from .models import Course, Tee, Hole
from .forms import CourseUpdateForm, TeeUpdateForm, HoleUpdateForm, CourseCreateForm, TeeCreateForm


#HELPER FUNCTIONS

def canEditCourse(request, course) -> bool:
    ''' Only allow user to make changes to a course if they
        1. Created the course and the course isn't verified
        2. Are a staff member '''
    
    creator = course.creator
    user = request.user
    is_staff = request.user.is_staff
    if course.verified:
        return is_staff
    else:
        return creator == user or is_staff


#VIEWS

@login_required
def courseList(request):
    courses = Course.objects.all()
    context = {"courses": courses}
    return render(request, 'courselibrary/courselibrary.html', context)


@login_required
def courseCreate(request):
    if request.method == 'POST':
        form = CourseCreateForm(request.POST)
        if form.is_valid():
            form.instance.creator = request.user
            form.save()
            messages.success(request, f'Course successfully created.')
            return redirect(reverse('courselibrary:edit', kwargs={ 'course_id': form.instance.id }))
    else:
        form = CourseCreateForm()

    context = {
        'form': form
    }
    return render(request, 'courselibrary/create.html', context)


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
    if canEditCourse(request, course) == False:
        raise PermissionDenied()

    if request.method == 'POST':
        form = CourseUpdateForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f'Course successfully updated.')
            return redirect(reverse('courselibrary:detail', kwargs={ 'course_id': course_id }))
    else:
        form = CourseUpdateForm(instance=course)

    context = {
        'course': course,
        'form': form,
        'tees': tees
    }

    return render(request, 'courselibrary/edit.html', context)


@login_required
def courseDelete(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    if canEditCourse(request, course) == False:
        raise PermissionDenied()

    if request.method == "POST":
        course.delete()
        return redirect('courselibrary:courselibrary')
    else:
        return render(request, "courselibrary/confirm_course_delete.html", {'course': course})


@login_required
def teeCreate(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    if canEditCourse(request, course) == False:
        raise PermissionDenied()
    
    num_holes = int(course.num_of_holes)
    HoleFormset = modelformset_factory(Hole, fields=('par', 'yards'), extra=num_holes)

    if request.method == 'POST':
        form = TeeCreateForm(request.POST)
        hole_formset = HoleFormset(request.POST, queryset=Hole.objects.none())
        if form.is_valid() and hole_formset.is_valid():
            form.instance.course = course
            form.save()

            hole_instances = hole_formset.save(commit=False)
            for hole_instance in hole_instances:
                hole_instance.number = 1
                hole_instance.tees = form.instance
                hole_instance.save()

            messages.success(request, f'Tee successfully created.')
            return redirect(reverse('courselibrary:edit', kwargs={ 'course_id': course.id }))
    else:
        form = TeeCreateForm()
        hole_formset = HoleFormset(queryset=Hole.objects.none())

    context = {
        'form': form,
        'hole_formset': hole_formset,
        'course': course,
    }

    return render(request, 'courselibrary/tee_create.html', context)


@login_required
def teeEdit(request, tee_id):
    try:
        tee = Tee.objects.get(pk=tee_id)
        course = tee.course
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    except Tee.DoesNotExist:
        raise Http404("Tee does not exist")
    if canEditCourse(request, course) == False:
        raise PermissionDenied()
    
    HoleFormset = modelformset_factory(Hole, fields=('par', 'yards'), extra=0)

    if request.method == 'POST':
        form = TeeUpdateForm(request.POST, instance=tee)
        hole_formset = HoleFormset(request.POST, queryset=Hole.objects.filter(tees=tee))
        if form.is_valid() and hole_formset.is_valid():
            form.save()
            hole_formset.save()
            messages.success(request, f'Tee successfully update.')
            return redirect(reverse('courselibrary:edit', kwargs={ 'course_id': course.id }))
    else:
        form = TeeUpdateForm(instance=tee)
        hole_formset = HoleFormset(queryset=Hole.objects.filter(tees=tee))

    context = {
        'tee': tee,
        'form': form,
        'hole_formset': hole_formset,
        'course': course
    }

    return render(request, 'courselibrary/tee_edit.html', context)


@login_required
def teeDelete(request, tee_id):
    try:
        tee = Tee.objects.get(pk=tee_id)
        course = tee.course
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    except Tee.DoesNotExist:
        raise Http404("Tee does not exist")
    if canEditCourse(request, course) == False:
        raise PermissionDenied()

    if request.method == "POST":
        tee.delete()
        return redirect(reverse('courselibrary:edit', kwargs={ 'course_id': course.id }))
    else:
        return render(request, "courselibrary/confirm_tee_delete.html", {'course': course})

