from django.db import models
from django.contrib.auth.models import User
from courselibrary.models import Course, Tee


class Round(models.Model):
    ROUND_CHOICES = {
        "F9": "Front 9",
        "B9": "Back 9",
        "18": "18 Holes"
    }

    player = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)
    tees = models.ForeignKey(Tee, on_delete=models.SET_NULL, blank=True, null=True)
    num_of_holes = models.CharField(max_length=2, choices=ROUND_CHOICES)
    datetime = models.DateTimeField(auto_now_add=True)
    weather_conditions = models.IntegerField(blank=True, null=True)
    public = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.course}, Round ID: {self.pk}'
    

class Score(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    hole_number = models.IntegerField()
    par = models.IntegerField()
    yardage = models.IntegerField()
    score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.round}, Hole: {self.hole_number}'
