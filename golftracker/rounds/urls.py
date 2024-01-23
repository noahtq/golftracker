from django.urls import path
from . import views

app_name = "rounds"
urlpatterns = [
    path('', views.welcome, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('roundslibrary/', views.RoundListView.as_view(), name='library'),
    path('roundslibrary/<int:pk>/', views.RoundDetailView.as_view(), name='detail'),
    path('roundslibrary/<int:pk>/update/', views.RoundUpdateView.as_view(), name='update'),
    path('roundslibrary/<int:pk>/delete/', views.RoundDeleteView.as_view(), name='delete'),
]