from django import forms
from .models import Course, Tee


class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'location', 'num_of_holes']


class CourseUpdateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'location', 'num_of_holes']


class TeeCreateForm(forms.ModelForm):
    class Meta:
        model = Tee
        fields = ['name', 'course_rating', 'slope_rating']


class TeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Tee
        fields = ['name', 'course_rating', 'slope_rating']
