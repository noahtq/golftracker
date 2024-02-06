from django import forms
from .models import Round, Score


class RoundCreateForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = ['course', 'tees', 'num_of_holes', 'weather_conditions', 'public']

    def clean_tees(self):
        tee = self.cleaned_data['tees']
        course = self.cleaned_data['course']
        print(tee, course)
        if tee.course != course:
            raise forms.ValidationError('Tee must match Course')
        return tee
