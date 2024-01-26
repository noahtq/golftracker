from django.urls import path
from . import views

app_name = "courselibrary"
urlpatterns = [
    path('', views.courseList, name='courselibrary'),
    path('<int:course_id>/', views.courseDetails, name='detail'),
    path('<int:course_id>/edit', views.courseEdit, name='edit'),
    path('<int:tee_id>/edittee/', views.teeEdit, name='tee-edit'),
]