from django.urls import path
from . import views

app_name = "courselibrary"
urlpatterns = [
    path('', views.CourseListView, name='courselibrary'),
]