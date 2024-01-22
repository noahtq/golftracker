from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Round


def welcome(request):
    return render(request, 'rounds/welcome.html')


@login_required
def dashboard(request):
    rounds = Round.objects.all()
    context = {"rounds": rounds}
    return render(request, 'rounds/dashboard.html', context)


class RoundListView(LoginRequiredMixin, generic.ListView):
    template_name = 'rounds/roundlist.html'
    context_object_name = 'rounds_list'

    def get_queryset(self) -> QuerySet[Any]:
        return Round.objects.filter(player=self.request.user).order_by('-datetime')[:100]