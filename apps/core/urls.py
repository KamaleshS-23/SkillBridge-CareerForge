from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('skill-gap-analysis/', views.skill_gap_analysis, name='skill_gap_analysis'),
    path('internship-finder/', views.internship_finder, name='internship_finder'),
    path('progress-tracking/', views.progress_tracking, name='progress_tracking'),
    path('api/get-role-requirements/', views.get_role_requirements, name='get_role_requirements'),
]