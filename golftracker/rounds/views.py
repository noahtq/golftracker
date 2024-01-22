from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Round


def welcome(request):
    return render(request, 'rounds/welcome.html')

@login_required
def dashboard(request):
    rounds = Round.objects.all()
    context = {"rounds": rounds}
    return render(request, 'rounds/dashboard.html', context)
