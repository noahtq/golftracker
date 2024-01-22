from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    HOLE_CHOICES = {
        "09": "9 Holes",
        "18": "18 Holes"
    }

    name = models.CharField(max_length=256)
    location = models.CharField(max_length=256, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    verified = models.BooleanField(default=False)
    num_of_holes = models.CharField(max_length=2, choices=HOLE_CHOICES)

    def __str__(self):
        return self.name
    

class Tee(models.Model):
    name = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_rating = models.FloatField(blank=True, null=True)
    slope_rating = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class Hole(models.Model):
    number = models.IntegerField()
    par = models.IntegerField()
    yards = models.IntegerField()
    tees = models.ForeignKey(Tee, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.number}'

