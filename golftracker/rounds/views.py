from django.shortcuts import render
from .models import Round

def roundListView(request):
    rounds = Round.objects.all()
    context = {"rounds": rounds}
    return render(request, 'rounds/dashboard.html', context)
