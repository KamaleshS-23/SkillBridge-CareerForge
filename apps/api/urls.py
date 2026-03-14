from django.urls import path
from apps.skills import views as skills_views
from apps.core import views as core_views

app_name = 'api'

urlpatterns = [
    # Professional Identity
    path('get-professional-identity/', skills_views.get_professional_identity, name='get_professional_identity'),
    path('save-professional-identity/', skills_views.save_professional_identity, name='save_professional_identity'),
    
    # Education
    path('add-education/', skills_views.add_education, name='add_education'),
    path('delete-education/<int:education_id>/', skills_views.delete_education, name='delete_education'),
    
    # Certifications
    path('add-certification/', skills_views.add_certification, name='add_certification'),
    path('delete-certification/<int:cert_id>/', skills_views.delete_certification, name='delete_certification'),
    
    # Courses
    path('add-course/', skills_views.add_course, name='add_course'),
    
    # Projects
    path('add-project/', skills_views.add_project, name='add_project'),
    path('delete-project/<int:project_id>/', skills_views.delete_project, name='delete_project'),
    
    # Skills
    path('add-skill/', skills_views.add_skill, name='add_skill'),
    path('get-role-requirements/', core_views.get_role_requirements, name='get_role_requirements'),
    
    # Languages
    path('add-language/', skills_views.add_language, name='add_language'),
]
