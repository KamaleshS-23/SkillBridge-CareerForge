from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import transaction
import json
import requests
from datetime import datetime

from .models import (
    ProfessionalIdentity, Education, Certification, Course, Skill,
    UserSkill, Project, Language, AIProfilingSession, SkillContextMetadata
)
from apps.accounts.models import User


@login_required(login_url='login')
def profile_page(request):
    """Render the AI Profiling page"""
    user = request.user
    
    # Get or create professional identity
    prof_identity, _ = ProfessionalIdentity.objects.get_or_create(user=user)
    
    # Get related data
    education = Education.objects.filter(user=user).order_by('-graduation_year')
    certifications = Certification.objects.filter(user=user).order_by('-issue_date')
    courses = Course.objects.filter(user=user).order_by('-completion_date')
    projects = Project.objects.filter(user=user).order_by('-start_date')
    languages = Language.objects.filter(user=user)
    skills = UserSkill.objects.filter(user=user).select_related('skill')
    profiling_sessions = AIProfilingSession.objects.filter(user=user).order_by('-started_at')
    context = {
        'user': user,
        'hide_sidebar': True,  # Keep the focused view
    }
    
    # Use AJAX-friendly template for dynamic loading
    return render(request, 'core/profilepage.html', context)


@login_required(login_url='login')
def skill_gap_page(request):
    """Render the Skill Gap Analysis page"""
    import json
    
    user = request.user
    
    # Get user's skills
    user_skills = UserSkill.objects.filter(user=user).select_related('skill')
    user_skills_data = [
        {
            'id': us.id,
            'name': us.skill.name,
            'proficiency': us.proficiency_level,
            'endorsements': us.endorsement_count or 0,
            'category': us.skill.category or 'General'
        }
        for us in user_skills
    ]
    
    # Get skill categories
    categories = set(s.get('category', 'General') for s in user_skills_data)
    categories_data = sorted(list(categories))
    
    context = {
        'user_skills_json': json.dumps(user_skills_data),
        'categories_json': json.dumps(categories_data)
    }
    return render(request, 'core/skillgap.html', context)


@login_required(login_url='login')
@require_http_methods(["GET"])
def get_professional_identity(request):
    """Retrieve professional identity data"""
    try:
        user = request.user
        prof_identity = ProfessionalIdentity.objects.get(user=user)
        
        return JsonResponse({
            'status': 'success',
            'data': {
                'fullName': prof_identity.full_name,
                'educationLevel': prof_identity.education_level,
                'dateOfBirth': str(prof_identity.date_of_birth) if prof_identity.date_of_birth else '',
                'gender': prof_identity.gender,
                'phoneNumber': prof_identity.phone_number,
                'location': prof_identity.location,
                'nativeLanguage': prof_identity.native_language,
                'linkedin': prof_identity.linkedin_url,
                'github': prof_identity.github_url,
                'portfolio': prof_identity.portfolio_url,
                'resume': prof_identity.resume_url,
            }
        })
    except ProfessionalIdentity.DoesNotExist:
        return JsonResponse({
            'status': 'success',
            'data': {}  # Return empty object if no identity exists yet
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required(login_url='login')
@require_http_methods(["POST"])
def save_professional_identity(request):
    """Save professional identity data"""
    try:
        data = json.loads(request.body)
        user = request.user
        
        prof_identity, _ = ProfessionalIdentity.objects.get_or_create(user=user)
        
        # Helper function to validate and clean URLs
        def clean_url(url_string):
            """Validate and clean URL - returns empty string if invalid"""
            if not url_string or not url_string.strip():
                return ''
            url_string = url_string.strip()
            # Only allow URLs that have actual content after the protocol
            if url_string in ['http://', 'https://', 'http', 'https']:
                return ''
            return url_string
        
        # Save all identity fields
        prof_identity.full_name = data.get('fullName', prof_identity.full_name) or ''
        prof_identity.education_level = data.get('educationLevel', '') or ''
        
        # Handle date of birth - accept string format
        dob = data.get('dateOfBirth')
        if dob and dob.strip():
            try:
                # If it's already a date string in YYYY-MM-DD format, use it directly
                prof_identity.date_of_birth = dob
            except:
                prof_identity.date_of_birth = None
        else:
            prof_identity.date_of_birth = None
        
        prof_identity.gender = data.get('gender', '') or ''
        prof_identity.phone_number = data.get('phoneNumber', '') or ''
        prof_identity.location = data.get('location', '') or ''
        prof_identity.native_language = data.get('nativeLanguage', '') or ''
        
        # Handle URLs with validation and cleaning
        prof_identity.linkedin_url = clean_url(data.get('linkedin_url') or data.get('linkedin', ''))
        prof_identity.github_url = clean_url(data.get('github_url') or data.get('github', ''))
        prof_identity.portfolio_url = clean_url(data.get('portfolio_url') or data.get('portfolio', ''))
        prof_identity.resume_url = clean_url(data.get('resume_url') or data.get('resume', ''))
        
        prof_identity.save()
        
        return JsonResponse({
            'status': 'success', 
            'message': 'Professional identity saved successfully',
            'data': {
                'full_name': prof_identity.full_name,
                'education_level': prof_identity.education_level,
                'date_of_birth': str(prof_identity.date_of_birth) if prof_identity.date_of_birth else '',
                'gender': prof_identity.gender,
                'phone_number': prof_identity.phone_number,
                'location': prof_identity.location,
                'native_language': prof_identity.native_language,
                'linkedin_url': prof_identity.linkedin_url,
                'github_url': prof_identity.github_url,
                'portfolio_url': prof_identity.portfolio_url,
                'resume_url': prof_identity.resume_url,
            }
        })
    except ValueError as ve:
        return JsonResponse({'status': 'error', 'message': f'Invalid data format: {str(ve)}'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error saving data: {str(e)}'}, status=400)


@login_required(login_url='login')
@require_http_methods(["POST"])
def add_education(request):
    """Add education record"""
    try:
        data = json.loads(request.body)
        user = request.user
        
        education = Education.objects.create(
            user=user,
            degree_type=data.get('degree_type'),
            field_of_study=data.get('field_of_study'),
            school_name=data.get('school_name'),
            graduation_year=int(data.get('graduation_year')),
            gpa=data.get('gpa') if data.get('gpa') else None,
            description=data.get('description', '')
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Education added',
            'id': education.id
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required(login_url='login')
@require_http_methods(["POST"])
def add_certification(request):
    """Add certification record"""
    try:
        data = json.loads(request.body)
        user = request.user
        
        cert = Certification.objects.create(
            user=user,
            certification_name=data.get('certification_name'),
            issuing_organization=data.get('issuing_organization'),
            issue_date=data.get('issue_date'),
            expiry_date=data.get('expiry_date') if data.get('expiry_date') else None,
            credential_id=data.get('credential_id', ''),
            credential_url=data.get('credential_url', ''),
            is_active=data.get('is_active', True)
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Certification added',
            'id': cert.id
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required(login_url='login')
@require_http_methods(["POST"])
def add_course(request):
    """Add course record"""
    try:
        data = json.loads(request.body)
        user = request.user
        
        course = Course.objects.create(
            user=user,
            course_name=data.get('course_name'),
            platform=data.get('platform'),
            completion_date=data.get('completion_date'),
            certificate_url=data.get('certificate_url', '')
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Course added',
            'id': course.id
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required(login_url='login')
@require_http_methods(["POST"])
def add_project(request):
    """Add project record"""
    try:
        data = json.loads(request.body)
        user = request.user
        
        project = Project.objects.create(
            user=user,
            project_name=data.get('project_name'),
            description=data.get('description'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date') if data.get('end_date') else None,
            is_active=data.get('is_active', False),
            project_url=data.get('project_url', ''),
            github_url=data.get('github_url', ''),
            team_size=int(data.get('team_size')) if data.get('team_size') else None,
            impact=data.get('impact', '')
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Project added',
            'id': project.id
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required(login_url='login')
@require_http_methods(["POST"])
def add_language(request):
    """Add language proficiency"""
    try:
        data = json.loads(request.body)
        user = request.user
        
        # Accept both 'proficiency' and 'proficiency_level'
        proficiency = data.get('proficiency') or data.get('proficiency_level', 'intermediate')
        
        language, created = Language.objects.update_or_create(
            user=user,
            language_name=data.get('language_name'),
            defaults={'proficiency': proficiency}
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Language added',
            'id': language.id
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required(login_url='login')
@require_http_methods(["POST"])
def add_skill(request):
    """Add or update user skill with metadata"""
    try:
        data = json.loads(request.body)
        user = request.user
        
        # Get or create skill
        skill_name = data.get('skill_name')
        # Accept both 'skill_type' and 'category' as the category field
        skill_type = data.get('skill_type') or data.get('category', 'technical')
        
        skill, _ = Skill.objects.get_or_create(
            name=skill_name,
            defaults={'skill_type': skill_type}
        )
        
        # Create or update UserSkill
        user_skill, created = UserSkill.objects.update_or_create(
            user=user,
            skill=skill,
            defaults={
                'proficiency_level': data.get('proficiency_level', 'intermediate'),
                'years_experience': float(data.get('years_experience', 0))
            }
        )
        
        # Create or update metadata
        if data.get('context_of_use') or data.get('source'):
            metadata, _ = SkillContextMetadata.objects.update_or_create(
                user_skill=user_skill,
                defaults={
                    'context_of_use': data.get('context_of_use', ''),
                    'frequency': data.get('frequency', 'occasional'),
                    'source': data.get('source', 'manual'),
                    'last_used_date': data.get('last_used_date') if data.get('last_used_date') else None
                }
            )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Skill added',
            'id': user_skill.id
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required(login_url='login')
@require_http_methods(["POST"])
def sync_linkedin(request):
    """Trigger LinkedIn profile sync"""
    try:
        data = json.loads(request.body)
        user = request.user
        linkedin_url = data.get('linkedin_url')
        
        if not linkedin_url:
            return JsonResponse({'status': 'error', 'message': 'LinkedIn URL is required'}, status=400)
        
        # Create a profiling session
        session = AIProfilingSession.objects.create(
            user=user,
            session_type='linkedin',
            source_url=linkedin_url,
            status='processing'
        )
        
        # Here you would integrate with LinkedIn API or parsing library
        # For now, we'll simulate the extraction
        try:
            # Update session with mock data
            session.status = 'completed'
            session.completed_at = timezone.now()
            session.skills_extracted = 0
            session.confidence_score = 0.85
            session.save()
            
            # Update professional identity
            prof_identity, _ = ProfessionalIdentity.objects.get_or_create(user=user)
            prof_identity.linkedin_url = linkedin_url
            prof_identity.last_linkedin_sync = timezone.now()
            prof_identity.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'LinkedIn synced successfully',
                'session_id': session.id
            })
        except Exception as e:
            session.status = 'failed'
            session.error_message = str(e)
            session.completed_at = timezone.now()
            session.save()
            raise
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required(login_url='login')
@require_http_methods(["POST"])
def sync_github(request):
    """Trigger GitHub profile sync"""
    try:
        data = json.loads(request.body)
        user = request.user
        github_url = data.get('github_url')
        
        if not github_url:
            return JsonResponse({'status': 'error', 'message': 'GitHub URL is required'}, status=400)
        
        session = AIProfilingSession.objects.create(
            user=user,
            session_type='github',
            source_url=github_url,
            status='processing'
        )
        
        try:
            # GitHub API integration would go here
            session.status = 'completed'
            session.completed_at = timezone.now()
            session.skills_extracted = 0
            session.confidence_score = 0.90
            session.save()
            
            prof_identity, _ = ProfessionalIdentity.objects.get_or_create(user=user)
            prof_identity.github_url = github_url
            prof_identity.last_github_sync = timezone.now()
            prof_identity.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'GitHub synced successfully',
                'session_id': session.id
            })
        except Exception as e:
            session.status = 'failed'
            session.error_message = str(e)
            session.completed_at = timezone.now()
            session.save()
            raise
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required(login_url='login')
@require_http_methods(["GET"])
def get_profiling_summary(request):
    """Get AI profiling summary"""
    try:
        user = request.user
        
        prof_identity = ProfessionalIdentity.objects.filter(user=user).first()
        education_count = Education.objects.filter(user=user).count()
        cert_count = Certification.objects.filter(user=user).filter(is_active=True).count()
        course_count = Course.objects.filter(user=user).count()
        project_count = Project.objects.filter(user=user).count()
        skill_count = UserSkill.objects.filter(user=user).count()
        language_count = Language.objects.filter(user=user).count()
        
        # Calculate profiling completion percentage
        total_fields = 8
        filled_fields = 0
        
        if prof_identity and prof_identity.full_name:
            filled_fields += 1
        if education_count > 0:
            filled_fields += 1
        if cert_count > 0:
            filled_fields += 1
        if course_count > 0:
            filled_fields += 1
        if project_count > 0:
            filled_fields += 1
        if skill_count > 0:
            filled_fields += 1
        if language_count > 0:
            filled_fields += 1
        if prof_identity and prof_identity.linkedin_url:
            filled_fields += 1
            
        completion_percentage = int((filled_fields / total_fields) * 100)
        
        return JsonResponse({
            'status': 'success',
            'data': {
                'education_count': education_count,
                'certification_count': cert_count,
                'course_count': course_count,
                'project_count': project_count,
                'skill_count': skill_count,
                'language_count': language_count,
                'completion_percentage': completion_percentage
            }
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required(login_url='login')
@require_http_methods(["DELETE"])
def delete_education(request, education_id):
    """Delete education record"""
    try:
        education = Education.objects.get(id=education_id, user=request.user)
        education.delete()
        return JsonResponse({'status': 'success', 'message': 'Education deleted'})
    except Education.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Education not found'}, status=404)


@login_required(login_url='login')
@require_http_methods(["DELETE"])
def delete_certification(request, cert_id):
    """Delete certification record"""
    try:
        cert = Certification.objects.get(id=cert_id, user=request.user)
        cert.delete()
        return JsonResponse({'status': 'success', 'message': 'Certification deleted'})
    except Certification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Certification not found'}, status=404)


@login_required(login_url='login')
@require_http_methods(["DELETE"])
def delete_project(request, project_id):
    """Delete project record"""
    try:
        project = Project.objects.get(id=project_id, user=request.user)
        project.delete()
        return JsonResponse({'status': 'success', 'message': 'Project deleted'})
    except Project.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Project not found'}, status=404)


@login_required(login_url='login')
@require_http_methods(["DELETE"])
def delete_skill(request, skill_id):
    """Delete user skill"""
    try:
        skill = UserSkill.objects.get(id=skill_id, user=request.user)
        skill.delete()
        return JsonResponse({'status': 'success', 'message': 'Skill deleted'})
    except UserSkill.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Skill not found'}, status=404)

