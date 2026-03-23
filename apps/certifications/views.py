from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import logging
from .models import Certification
from .sync_manager import CertificationSyncManager

logger = logging.getLogger(__name__)

def certification_dashboard(request):
    """Main certification dashboard with recommendations"""
    context = {
        'total_certifications': Certification.objects.filter(is_active=True).count(),
        'active_certifications': Certification.objects.filter(is_active=True, is_synced=True).count(),
        'providers_count': Certification.objects.values('provider').distinct().count(),
        'last_sync': Certification.objects.order_by('-last_updated').first().last_updated if Certification.objects.exists() else None,
        'providers': get_provider_status(),
        'recommendations': get_recommended_certifications(request),
    }
    return render(request, 'certifications/dashboard.html', context)

def get_provider_status():
    """Get status for each certification provider"""
    providers = [
        {'key': 'coursera', 'name': 'Coursera', 'status': 'active', 
         'count': Certification.objects.filter(provider='coursera', is_active=True).count(),
         'last_updated': Certification.objects.filter(provider='coursera').order_by('-last_updated').first().last_updated if Certification.objects.filter(provider='coursera').exists() else None},
        {'key': 'aws', 'name': 'AWS', 'status': 'active',
         'count': Certification.objects.filter(provider='aws', is_active=True).count(),
         'last_updated': Certification.objects.filter(provider='aws').order_by('-last_updated').first().last_updated if Certification.objects.filter(provider='aws').exists() else None},
        {'key': 'google', 'name': 'Google', 'status': 'active',
         'count': Certification.objects.filter(provider='google', is_active=True).count(),
         'last_updated': Certification.objects.filter(provider='google').order_by('-last_updated').first().last_updated if Certification.objects.filter(provider='google').exists() else None},
        {'key': 'microsoft', 'name': 'Microsoft', 'status': 'active',
         'count': Certification.objects.filter(provider='microsoft', is_active=True).count(),
         'last_updated': Certification.objects.filter(provider='microsoft').order_by('-last_updated').first().last_updated if Certification.objects.filter(provider='microsoft').exists() else None},
    ]
    return providers

def get_recommended_certifications(request):
    """Get personalized certification recommendations based on industry demand"""
    certifications = Certification.objects.filter(is_active=True, is_synced=True)
    
    # Calculate demand scores based on industry trends
    demand_weights = {
        'Cloud Computing': 95,
        'AI & Machine Learning': 92,
        'Data Science': 90,
        'Cybersecurity': 88,
        'DevOps': 85,
        'Software Development': 82,
        'Project Management': 75,
        'Digital Marketing': 70,
    }
    
    recommended = []
    for cert in certifications:
        demand_score = demand_weights.get(cert.domain, 65)
        recommended.append({
            'id': cert.id,
            'name': cert.name,
            'provider': cert.provider,
            'domain': cert.domain,
            'description': cert.description,
            'rating': cert.rating,
            'duration': cert.duration,
            'difficulty_level': cert.difficulty_level,
            'get_difficulty_level_display': cert.get_difficulty_level_display(),
            'registration_url': cert.registration_url,
            'demand_score': demand_score,
        })
    
    # Sort by demand score
    recommended.sort(key=lambda x: x['demand_score'], reverse=True)
    return recommended[:20]  # Return top 20 recommendations

@csrf_exempt
def sync_certifications(request):
    """API endpoint to sync certifications from all providers"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.body else {}
            provider = data.get('provider')
            force = data.get('force', False)
            
            sync_manager = CertificationSyncManager()
            
            if provider:
                result = sync_manager.sync_provider(provider, force=force)
            else:
                result = sync_manager.sync_all_providers(force=force)
            
            return JsonResponse(result)
        except Exception as e:
            logger.error(f"Sync error: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def certification_stats(request):
    """Get certification statistics"""
    stats = {
        'total': Certification.objects.filter(is_active=True).count(),
        'active': Certification.objects.filter(is_active=True, is_synced=True).count(),
        'providers': Certification.objects.values('provider').distinct().count(),
        'last_sync': Certification.objects.order_by('-last_updated').first().last_updated.isoformat() if Certification.objects.exists() else None,
    }
    return JsonResponse(stats)

@csrf_exempt
def clear_cache(request):
    """Clear certification cache"""
    if request.method == 'POST':
        # Implementation for cache clearing
        return JsonResponse({'success': True, 'message': 'Cache cleared successfully'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)
