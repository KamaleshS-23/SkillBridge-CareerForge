from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('skill-gap-analysis/', views.skill_gap_analysis, name='skill_gap_analysis'),
    path('internship-finder/', views.internship_finder, name='internship_finder'),
    path('progress-tracking/', views.progress_tracking, name='progress_tracking'),
    path('ai-mock-interview/', views.ai_mock_interview, name='ai_mock_interview'),
    path('roadmap/', views.roadmap, name='roadmap'),
    path('certification/', views.certification_recommendations, name='certification_recommendations'),
    path('technical/', views.technical_assessment, name='technical_assessment'),
    path('resume-builder/', views.resume_builder, name='resume_builder'),
    path('aptitude/', views.aptitude_test, name='aptitude_test'),
    path('api/get-role-requirements/', views.get_role_requirements, name='get_role_requirements'),
]