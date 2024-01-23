from django import forms
from .models import Course, Tee, Hole


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