from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json

def roadmap_view(request):
    """
    Render the roadmap page
    """
    # Allow access to template, but API calls will require login
    return render(request, 'core/roadmap.html')


@login_required
def roadmap_data_api(request):
    """
    API endpoint to get roadmap categories and user progress
    """
    try:
        from apps.core.models import RoadmapCategory, RoadmapItem, UserRoadmapProgress
        
        # Get all categories with their items
        categories = RoadmapCategory.objects.all().prefetch_related('items')
        
        categories_data = []
        for category in categories:
            items_data = []
            for item in category.items.all():
                items_data.append({
                    'id': item.id,
                    'title': item.title,
                    'description': item.description,
                    'difficulty': item.difficulty,
                    'estimated_hours': item.estimated_hours,
                    'resources': item.resources or {}
                })
            
            categories_data.append({
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'icon': category.icon,
                'items': items_data
            })
        
        # Get user progress
        user_progress = UserRoadmapProgress.objects.filter(user=request.user)
        progress_data = {}
        
        for progress in user_progress:
            progress_data[str(progress.roadmap_item.id)] = {
                'completed': progress.completed,
                'completed_at': progress.completed_at.isoformat() if progress.completed_at else None,
                'notes': progress.notes,
                'rating': progress.rating
            }
        
        return JsonResponse({
            'categories': categories_data,
            'user_progress': progress_data
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@login_required
@require_http_methods(["POST"])
def roadmap_update_progress_api(request):
    """
    API endpoint to update user roadmap progress
    """
    try:
        from apps.core.models import RoadmapItem, UserRoadmapProgress
        from django.utils import timezone
        
        data = json.loads(request.body)
        item_id = data.get('item_id')
        completed = data.get('completed', False)
        
        if not item_id:
            return JsonResponse({
                'success': False,
                'message': 'item_id is required'
            }, status=400)
        
        # Get the roadmap item
        roadmap_item = RoadmapItem.objects.get(id=item_id)
        
        # Get or create user progress
        user_progress, created = UserRoadmapProgress.objects.get_or_create(
            user=request.user,
            roadmap_item=roadmap_item,
            defaults={
                'completed': completed,
                'completed_at': timezone.now() if completed else None
            }
        )
        
        if not created:
            user_progress.completed = completed
            user_progress.completed_at = timezone.now() if completed else None
            user_progress.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Progress updated successfully'
        })
        
    except RoadmapItem.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Roadmap item not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)
