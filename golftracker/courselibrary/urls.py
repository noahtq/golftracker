from django.urls import path
from . import views

app_name = "courselibrary"
urlpatterns = [
    path('', views.courseList, name='courselibrary'),
    path('create/', views.courseCreate, name='create'),
    path('<int:course_id>/', views.courseDetails, name='detail'),
    path('<int:course_id>/edit/', views.courseEdit, name='edit'),
    path('<int:course_id>/delete/', views.courseDelete, name='delete'),
    path('<int:course_id>/newtee/', views.teeCreate, name='tee-create'),
    path('<int:tee_id>/edittee/', views.teeEdit, name='tee-edit'),
    path('<int:tee_id>/deletetee/', views.teeDelete, name='tee-delete'),
]