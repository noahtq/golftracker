from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.forms import modelformset_factory

from .forms import RoundCreateForm
from .models import Round, Score

'''HELPER FUNCTIONS'''

def isOwnerOrPublic(round, user) -> bool:
    ''' Check if user is the owner of the round or the round is public '''
    public = round.public
    owner = round.player
    return owner == user or public


def isOwner(round, user) -> bool:
    ''' Check if user is the owner of the round '''
    return user == round.player


def createScoreCard(round, tee) -> None:
    holes_nums = []
    if round.num_of_holes == 'F9':
        holes_nums = range(1, 10)
    elif round.num_of_holes == 'B9':
        holes_nums = range(10, 19)
    else:
        holes_nums = range(1, 19)
    holes_info = tee.hole_set.all()
    for i in holes_nums:
        hole_info = holes_info[i - 1]
        Score.objects.create(round=round, hole_number=i, par=hole_info.par, yardage=hole_info.yards)


'''VIEWS'''

def welcome(request):
    return render(request, 'rounds/welcome.html')


@login_required
def dashboard(request):
    rounds = Round.objects.all()
    context = {"rounds": rounds}
    return render(request, 'rounds/dashboard.html', context)


@login_required
def createRound(request):
    if request.method == 'POST':
        form = RoundCreateForm(request.POST)
        if form.is_valid():
            form.instance.player = request.user
            form.save()

            #Create associated scorecard with round as a series of score objects
            round_id = form.instance.pk
            try:
                tee = form.instance.tees
                round = Round.objects.get(pk=round_id)
                createScoreCard(round, tee)
            except:
                return HttpResponse(status=500)
            
            messages.success(request, f'Round successfully created.')
            return redirect(reverse('rounds:score-edit', kwargs={ 'round_id': round_id }))
    else:
        form = RoundCreateForm()

    context = {
        'form': form
    }
    return render(request, 'rounds/create_round.html', context)


@login_required
def scoreEdit(request, round_id):
    try:
        round = Round.objects.get(pk=round_id)
        scores = round.score_set.all()
    except Round.DoesNotExist:
        raise Http404("Round does not exist")
    if round.player != request.user:
        raise PermissionDenied()
    
    ScoreFormset = modelformset_factory(Score, fields=('score',), extra=0)

    if request.method == 'POST':
        score_formset = ScoreFormset(request.POST, queryset=Score.objects.filter(round=round))
        if score_formset.is_valid():
            score_formset.save()
            messages.success(request, f'Round successfully saved.')
            return redirect(reverse('rounds:detail', args=[str(round.pk)]))
    else:
        score_formset = ScoreFormset(queryset=Score.objects.filter(round=round))

    context = {
        'scores': scores,
        'round': round,
        'score_formset': score_formset
    }

    return render(request, 'rounds/score_edit.html', context)


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
    

class RoundUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Round
    fields = ['course', 'tees', 'num_of_holes', 'weather_conditions', 'public']
    template_name = "rounds/round_update.html"

    def get(self, request, *args, **kwargs):
        #Only show page if the round is public or user is the owner of the round
        if isOwner(self.get_object(), self.request.user) == False:
            raise PermissionDenied()
        return super().get(request, *args, **kwargs)
    
    def get_success_url(self) -> str:
        return reverse('rounds:detail', args=[str(self.get_object().pk)])
    

class RoundDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Round

    def get(self, request, *args, **kwargs):
        #Only show page if the round is public or user is the owner of the round
        if isOwner(self.get_object(), self.request.user) == False:
            raise PermissionDenied()
        return super().get(request, *args, **kwargs)
    
    def get_success_url(self) -> str:
        return reverse('rounds:library')

