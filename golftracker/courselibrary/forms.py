from django import forms
from django.forms import inlineformset_factory
from .models import Course, Tee, Hole


class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'location', 'num_of_holes']


class CourseUpdateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'location', 'num_of_holes']


class TeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Tee
        fields = ['name', 'course_rating', 'slope_rating']


class HoleUpdateForm(forms.ModelForm):
    class Meta:
        model = Hole
        fields = ['par', 'yards']

TeeFormSet = inlineformset_factory(Course, Tee, fields=('name', 'course_rating', 'slope_rating'), extra=0)