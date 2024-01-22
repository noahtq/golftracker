from django.urls import path
from . import views

app_name = "rounds"
urlpatterns = [
    path('', views.welcome, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('library/', views.RoundListView.as_view(), name='library')
]