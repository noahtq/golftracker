from django.shortcuts import render

from .models import Course

def CourseListView(request):
    courses = Course.objects.all()
    context = {"courses": courses}
    return render(request, 'courselibrary/courselibrary.html', context)

