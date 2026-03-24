from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone
import json
from apps.skills.models import UserSkill, Skill, SkillCategory, UserRoadmapProgress
from apps.jobs.models import Job
from .models import Internship, UserInternship, SavedInternship


class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add your context data here
        context['page_title'] = 'Home'
        context['page_description'] = 'Welcome to Career Forge'
        return context

def dashboard(request):
    return render(request, 'core/dashboard.html')


def roadmap(request):
    """
    Skill Roadmap Page - Choose Your Career Path
    Interactive career roadmaps with comprehensive skill tracking and learning resources
    """
    context = {
        'page_title': 'Skill Roadmap',
        'page_description': 'Choose your career path and follow comprehensive skill roadmaps with learning resources',
    }
    return render(request, 'core/roadmap.html', context)


@login_required
@require_http_methods(["POST"])
def save_roadmap_progress(request):
    """
    Save user's roadmap progress to database
    Expects: {career_path, category_name, skill_name, is_completed, category_index, skill_index}
    """
    try:
        data = json.loads(request.body)
        career_path = data.get('career_path', '').strip()
        category_name = data.get('category_name', '').strip()
        skill_name = data.get('skill_name', '').strip()
        is_completed = data.get('is_completed', False)
        category_index = data.get('category_index', 0)
        skill_index = data.get('skill_index', 0)
        
        if not all([career_path, category_name, skill_name]):
            return JsonResponse({
                'status': 'error',
                'message': 'Missing required fields: career_path, category_name, skill_name'
            }, status=400)
        
        # Get or create progress record
        progress, created = UserRoadmapProgress.objects.get_or_create(
            user=request.user,
            career_path=career_path,
            skill_name=skill_name,
            defaults={
                'category_name': category_name,
                'is_completed': is_completed,
                'category_index': category_index,
                'skill_index': skill_index,
                'completed_at': timezone.now() if is_completed else None
            }
        )
        
        if not created:
            # Update existing record
            progress.category_name = category_name
            progress.is_completed = is_completed
            progress.category_index = category_index
            progress.skill_index = skill_index
            if is_completed and not progress.completed_at:
                progress.completed_at = timezone.now()
            elif not is_completed:
                progress.completed_at = None
            progress.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Progress saved successfully',
            'created': created,
            'is_completed': progress.is_completed,
            'completed_at': progress.completed_at.isoformat() if progress.completed_at else None
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def load_roadmap_progress(request):
    """
    Load user's roadmap progress for a specific career path
    Query param: career_path
    """
    try:
        career_path = request.GET.get('career_path', '').strip()
        
        if not career_path:
            return JsonResponse({
                'status': 'error',
                'message': 'career_path parameter is required'
            }, status=400)
        
        # Get all progress for this career path
        progress_records = UserRoadmapProgress.objects.filter(
            user=request.user,
            career_path=career_path
        ).order_by('category_index', 'skill_index')
        
        # Format as {skill_name: is_completed} for easy lookup
        progress_data = {}
        for record in progress_records:
            progress_data[record.skill_name] = {
                'is_completed': record.is_completed,
                'category_name': record.category_name,
                'category_index': record.category_index,
                'skill_index': record.skill_index,
                'completed_at': record.completed_at.isoformat() if record.completed_at else None
            }
        
        return JsonResponse({
            'status': 'success',
            'career_path': career_path,
            'progress': progress_data,
            'total_skills': len(progress_data),
            'completed_skills': len([r for r in progress_records if r.is_completed])
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@login_required
@require_http_methods(["POST"])
def bulk_update_roadmap_progress(request):
    """
    Bulk update roadmap progress for multiple skills
    Expects: {career_path, updates: [{skill_name, is_completed, category_name, category_index, skill_index}]}
    """
    try:
        data = json.loads(request.body)
        career_path = data.get('career_path', '').strip()
        updates = data.get('updates', [])
        
        if not career_path or not updates:
            return JsonResponse({
                'status': 'error',
                'message': 'career_path and updates are required'
            }, status=400)
        
        updated_count = 0
        created_count = 0
        
        for update in updates:
            skill_name = update.get('skill_name', '').strip()
            if not skill_name:
                continue
                
            progress, created = UserRoadmapProgress.objects.get_or_create(
                user=request.user,
                career_path=career_path,
                skill_name=skill_name,
                defaults={
                    'category_name': update.get('category_name', ''),
                    'is_completed': update.get('is_completed', False),
                    'category_index': update.get('category_index', 0),
                    'skill_index': update.get('skill_index', 0),
                    'completed_at': timezone.now() if update.get('is_completed', False) else None
                }
            )
            
            if created:
                created_count += 1
            else:
                # Update existing record
                progress.category_name = update.get('category_name', progress.category_name)
                progress.is_completed = update.get('is_completed', progress.is_completed)
                progress.category_index = update.get('category_index', progress.category_index)
                progress.skill_index = update.get('skill_index', progress.skill_index)
                if progress.is_completed and not progress.completed_at:
                    progress.completed_at = timezone.now()
                elif not progress.is_completed:
                    progress.completed_at = None
                progress.save()
                updated_count += 1
        
        return JsonResponse({
            'status': 'success',
            'message': f'Bulk update completed: {created_count} created, {updated_count} updated',
            'created_count': created_count,
            'updated_count': updated_count,
            'total_processed': len(updates)
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
