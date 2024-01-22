from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.core.exceptions import PermissionDenied
from .models import Round


#Check if user is the owner of the round or the round is public
def isOwnerOrPublic(round, user):
    public = round.public
    owner = round.player
    return owner == user or public


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
    

class RoundDetailView(LoginRequiredMixin, generic.DetailView):
    model = Round
    template_name = "rounds/round_detail.html"

    def get(self, request, *args, **kwargs):
        #Only show page if the round is public or user is the owner of the round
        if isOwnerOrPublic(self.get_object(), self.request.user) == False:
            raise PermissionDenied()
        return super().get(request, *args, **kwargs)
