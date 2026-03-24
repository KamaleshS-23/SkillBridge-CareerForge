from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.utils import timezone

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def add_education(request):
    """Add education to user profile"""
    try:
        from apps.skills.models import Education
        
        data = json.loads(request.body)
        
        education = Education.objects.create(
            user=request.user,
            degree_type=data.get('degree_type', 'bachelor'),
            field_of_study=data.get('field_of_study', ''),
            school_name=data.get('school_name', ''),
            graduation_year=data.get('graduation_year') or 2024,  # Handle empty string
            gpa=data.get('gpa'),
            description=data.get('description', '')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Education added successfully',
            'education_id': education.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def add_certification(request):
    """Add certification to user profile"""
    try:
        from apps.skills.models import Certification
        
        data = json.loads(request.body)
        
        certification = Certification.objects.create(
            user=request.user,
            certification_name=data.get('certification_name', ''),
            issuing_organization=data.get('issuing_organization', ''),
            issue_date=data.get('issue_date') if data.get('issue_date') else None,  # Handle empty string
            expiry_date=data.get('expiry_date') if data.get('expiry_date') else None,  # Handle empty string
            credential_id=data.get('credential_id', ''),
            credential_url=data.get('credential_url', '')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Certification added successfully',
            'certification_id': certification.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def add_project(request):
    """Add project to user profile"""
    try:
        from apps.skills.models import Project
        
        data = json.loads(request.body)
        
        project = Project.objects.create(
            user=request.user,
            project_name=data.get('project_name', ''),
            description=data.get('description', ''),
            start_date=data.get('start_date') if data.get('start_date') else None,  # Handle empty string
            end_date=data.get('end_date') if data.get('end_date') else None,  # Handle empty string
            is_active=data.get('is_active', False),
            project_url=data.get('project_url', ''),
            github_url=data.get('github_url', ''),
            team_size=data.get('team_size'),
            impact=data.get('impact', '')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Project added successfully',
            'project_id': project.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def add_skill(request):
    """Add skill to user profile"""
    try:
        from apps.skills.models import UserSkill, Skill, SkillCategory
        
        data = json.loads(request.body)
        
        skill_name = data.get('skill_name', '')
        skill_level = data.get('proficiency_level', 'beginner')
        
        # Get or create skill category
        category, created = SkillCategory.objects.get_or_create(
            name='General',
            defaults={'description': 'General skills'}
        )
        
        # Get or create skill
        skill, created = Skill.objects.get_or_create(
            name=skill_name,
            defaults={
                'category': category,
                'skill_type': 'technical',
                'description': f'Skill in {skill_name}'
            }
        )
        
        # Create user skill with get_or_create to handle duplicates
        user_skill, created = UserSkill.objects.get_or_create(
            user=request.user,
            skill=skill,
            defaults={
                'proficiency_level': skill_level,
                'years_experience': data.get('years_experience', 0)
            }
        )
        
        if not created:
            # Update existing skill if needed
            user_skill.proficiency_level = skill_level
            user_skill.years_experience = data.get('years_experience', 0)
            user_skill.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Skill added successfully',
            'skill_id': user_skill.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def update_profile(request):
    """Update user profile information"""
    try:
        from apps.skills.models import ProfessionalIdentity
        
        data = json.loads(request.body)
        
        # Get or create professional identity
        profile, created = ProfessionalIdentity.objects.get_or_create(
            user=request.user,
            defaults={
                'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.email
            }
        )
        
        # Update profile fields
        if 'full_name' in data:
            profile.full_name = data['full_name']
        if 'education_level' in data:
            profile.education_level = data['education_level']
        if 'phone_number' in data:
            profile.phone_number = data['phone_number']
        if 'location' in data:
            profile.location = data['location']
        if 'native_language' in data:
            profile.native_language = data['native_language']
        if 'linkedin_url' in data:
            profile.linkedin_url = data['linkedin_url']
        if 'github_url' in data:
            profile.github_url = data['github_url']
        if 'portfolio_url' in data:
            profile.portfolio_url = data['portfolio_url']
        if 'resume_url' in data:
            profile.resume_url = data['resume_url']
        
        profile.save()
        
        # Update user model fields
        if 'first_name' in data:
            request.user.first_name = data['first_name']
        if 'last_name' in data:
            request.user.last_name = data['last_name']
        if 'email' in data:
            request.user.email = data['email']
        request.user.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Profile updated successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def add_language(request):
    """Add language to user profile"""
    try:
        from apps.skills.models import Language
        
        data = json.loads(request.body)
        
        language = Language.objects.create(
            user=request.user,
            language_name=data.get('language_name', ''),
            proficiency=data.get('proficiency_level', 'intermediate')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Language added successfully',
            'language_id': language.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["GET"])
def get_professional_identity(request):
    """Get professional identity for the current user"""
    try:
        from apps.skills.models import ProfessionalIdentity
        
        try:
            profile = ProfessionalIdentity.objects.get(user=request.user)
            return JsonResponse({
                'status': 'success',
                'data': {
                    'full_name': profile.full_name,
                    'education_level': profile.education_level,
                    'phone_number': profile.phone_number,
                    'location': profile.location,
                    'native_language': profile.native_language,
                    'linkedin_url': profile.linkedin_url,
                    'github_url': profile.github_url,
                    'portfolio_url': profile.portfolio_url,
                    'resume_url': profile.resume_url
                }
            })
        except ProfessionalIdentity.DoesNotExist:
            return JsonResponse({
                'status': 'success',
                'data': {}
            })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def save_professional_identity(request):
    """Save professional identity for the current user"""
    try:
        from apps.skills.models import ProfessionalIdentity
        
        data = json.loads(request.body)
        
        # Get or create professional identity
        profile, created = ProfessionalIdentity.objects.get_or_create(
            user=request.user,
            defaults={
                'full_name': data.get('fullName', ''),
                'education_level': data.get('educationLevel', ''),
                'phone_number': data.get('phoneNumber', ''),
                'location': data.get('location', ''),
                'native_language': data.get('nativeLanguage', ''),
                'linkedin_url': data.get('linkedin', ''),
                'github_url': data.get('github', ''),
                'portfolio_url': data.get('portfolio', ''),
                'resume_url': data.get('resume', '')
            }
        )
        
        # Update fields if not newly created
        if not created:
            profile.full_name = data.get('fullName', profile.full_name)
            profile.education_level = data.get('educationLevel', profile.education_level)
            profile.phone_number = data.get('phoneNumber', profile.phone_number)
            profile.location = data.get('location', profile.location)
            profile.native_language = data.get('nativeLanguage', profile.native_language)
            profile.linkedin_url = data.get('linkedin', profile.linkedin_url)
            profile.github_url = data.get('github', profile.github_url)
            profile.portfolio_url = data.get('portfolio', profile.portfolio_url)
            profile.resume_url = data.get('resume', profile.resume_url)
            profile.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Professional identity saved successfully',
            'data': {
                'full_name': profile.full_name,
                'education_level': profile.education_level,
                'phone_number': profile.phone_number,
                'location': profile.location,
                'native_language': profile.native_language,
                'linkedin_url': profile.linkedin_url,
                'github_url': profile.github_url,
                'portfolio_url': profile.portfolio_url,
                'resume_url': profile.resume_url
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def add_course(request):
    """Add course to user profile"""
    try:
        from apps.skills.models import Course
        
        data = json.loads(request.body)
        
        course = Course.objects.create(
            user=request.user,
            course_name=data.get('course_name', ''),
            platform=data.get('platform', ''),
            completion_date=data.get('completion_date') if data.get('completion_date') else None,  # Handle empty string
            certificate_url=data.get('certificate_url', '')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Course added successfully',
            'course_id': course.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)
