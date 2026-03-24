from django.urls import path
from . import views
from . import aptitude_views
from . import views_roadmap
from . import profile_api

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('skill-gap-analysis/', views.skill_gap_analysis, name='skill_gap_analysis'),
    path('internship/', views.simple_internship_view, name='internship_finder'),
    path('internship-finder/', views.simple_internship_view, name='internship_finder_alias'),
    path('my-internships/', views.my_internships, name='my_internships'),
    path('progress-tracking/', views.progress_tracking, name='progress_tracking'),
    path('ai-mock-interview/', views.ai_mock_interview, name='ai_mock_interview'),
    path('roadmap/', views_roadmap.roadmap_view, name='roadmap'),
    path('certification/', views.certification_recommendations, name='certification_recommendations'),
    path('technical/', views.technical_assessment, name='technical_assessment'),
    path('resume-builder/', views.resume_builder, name='resume_builder'),
    path('profile/', views.profilepage, name='profilepage'),
    path('aptitude/', views.aptitude_test, name='aptitude_test'),
    
    # API endpoints
    path('api/my-internships/', views.my_internships, name='api_my_internships'),
    path('api/get-role-requirements/', views.get_role_requirements, name='get_role_requirements'),
    path('api/enroll-internship/<int:internship_id>/', views.enroll_internship, name='enroll_internship'),
    path('api/update-internship/<int:enrollment_id>/', views.update_internship_status, name='update_internship_status'),
    path('api/save-internship/<int:internship_id>/', views.save_internship, name='save_internship'),
    path('api/unsave-internship/<int:internship_id>/', views.unsave_internship, name='unsave_internship'),
    path('api/internship-stats/', views.get_internship_stats, name='get_internship_stats'),
    
    # Profile API endpoints
    path('api/add-education/', profile_api.add_education, name='add_education'),
    path('api/add-certification/', profile_api.add_certification, name='add_certification'),
    path('api/add-project/', profile_api.add_project, name='add_project'),
    path('api/add-skill/', profile_api.add_skill, name='add_skill'),
    path('api/add-language/', profile_api.add_language, name='add_language'),
    path('api/add-course/', profile_api.add_course, name='add_course'),
    path('api/update-profile/', profile_api.update_profile, name='update_profile'),
    path('api/get-professional-identity/', profile_api.get_professional_identity, name='get_professional_identity'),
    path('api/save-professional-identity/', profile_api.save_professional_identity, name='save_professional_identity'),
    
    # Aptitude Test API endpoints
    path('api/submit-aptitude-test/', views.submit_aptitude_test, name='submit_aptitude_test'),
    path('api/aptitude-results/', views.get_aptitude_results, name='get_aptitude_results'),
    
    # Technical Test API endpoints
    path('api/submit-technical-test/', views.submit_technical_test, name='submit_technical_test'),
    path('api/technical-test-results/', views.get_technical_test_results, name='get_technical_test_results'),
    path('api/technical-test-stats/', views.get_technical_test_stats, name='get_technical_test_stats'),
    
    # Roadmap API endpoints
    path('api/roadmap/data/', views_roadmap.roadmap_data_api, name='roadmap_data_api'),
    path('api/roadmap/update-progress/', views_roadmap.roadmap_update_progress_api, name='roadmap_update_progress_api'),
    path('api/roadmap/save-progress/', views.save_roadmap_progress, name='save_roadmap_progress'),
    path('api/roadmap/load-progress/', views.load_roadmap_progress, name='load_roadmap_progress'),
    path('api/roadmap/bulk-update/', views.bulk_update_roadmap_progress, name='bulk_update_roadmap_progress'),
    
    # Progress Tracking API endpoints
    path('api/skill-gap-data/', views.skill_gap_data, name='skill_gap_data'),
    path('api/profile-data/', views.profile_data, name='profile_data'),
]