from django.urls import path
from . import views

app_name = 'skills'

urlpatterns = [
    # Profile Page
    path('profile/', views.profile_page, name='profile_page'),
    
    # Skill Gap Analysis Page
    path('skill-gap/', views.skill_gap_page, name='skill_gap'),
    
    # Professional Identity
    path('api/get-professional-identity/', views.get_professional_identity, name='get_professional_identity'),
    path('api/save-professional-identity/', views.save_professional_identity, name='save_professional_identity'),
    
    # Education
    path('api/add-education/', views.add_education, name='add_education'),
    path('api/delete-education/<int:education_id>/', views.delete_education, name='delete_education'),
    
    # Certifications
    path('api/add-certification/', views.add_certification, name='add_certification'),
    path('api/delete-certification/<int:cert_id>/', views.delete_certification, name='delete_certification'),
    
    # Courses
    path('api/add-course/', views.add_course, name='add_course'),
    
    # Projects
    path('api/add-project/', views.add_project, name='add_project'),
    path('api/delete-project/<int:project_id>/', views.delete_project, name='delete_project'),
    
    # Languages
    path('api/add-language/', views.add_language, name='add_language'),
    
    # Skills
    path('api/add-skill/', views.add_skill, name='add_skill'),
    path('api/delete-skill/<int:skill_id>/', views.delete_skill, name='delete_skill'),
    
    # Syncing
    path('api/sync-linkedin/', views.sync_linkedin, name='sync_linkedin'),
    path('api/sync-github/', views.sync_github, name='sync_github'),
    
    # Summary
    path('api/profiling-summary/', views.get_profiling_summary, name='profiling_summary'),
]
