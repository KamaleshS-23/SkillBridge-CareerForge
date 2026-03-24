from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import json
import logging
from .models import Certification
from .certification_fetchers import CertificationFetcher

logger = logging.getLogger(__name__)

@login_required
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
         'count': Certification.objects.filter(provider='Coursera', is_active=True).count(),
         'last_updated': Certification.objects.filter(provider='Coursera').order_by('-last_updated').first().last_updated if Certification.objects.filter(provider='Coursera').exists() else None},
        {'key': 'aws', 'name': 'AWS', 'status': 'active',
         'count': Certification.objects.filter(provider='AWS', is_active=True).count(),
         'last_updated': Certification.objects.filter(provider='AWS').order_by('-last_updated').first().last_updated if Certification.objects.filter(provider='AWS').exists() else None},
        {'key': 'google', 'name': 'Google Cloud', 'status': 'active',
         'count': Certification.objects.filter(provider='Google Cloud', is_active=True).count(),
         'last_updated': Certification.objects.filter(provider='Google Cloud').order_by('-last_updated').first().last_updated if Certification.objects.filter(provider='Google Cloud').exists() else None},
        {'key': 'microsoft', 'name': 'Microsoft', 'status': 'active',
         'count': Certification.objects.filter(provider='Microsoft', is_active=True).count(),
         'last_updated': Certification.objects.filter(provider='Microsoft').order_by('-last_updated').first().last_updated if Certification.objects.filter(provider='Microsoft').exists() else None},
        {'key': 'cisco', 'name': 'Cisco', 'status': 'active',
         'count': Certification.objects.filter(provider='Cisco', is_active=True).count(),
         'last_updated': Certification.objects.filter(provider='Cisco').order_by('-last_updated').first().last_updated if Certification.objects.filter(provider='Cisco').exists() else None},
    ]
    return providers

def get_recommended_certifications(request):
    """Get personalized certification recommendations based on industry demand"""
    certifications = Certification.objects.filter(is_active=True, is_synced=True)
    
    # Calculate demand scores based on industry trends
    demand_weights = {
        'Cloud Computing': 95,
        'Data Science': 92,
        'AI & Machine Learning': 90,
        'Cybersecurity': 88,
        'DevOps': 85,
        'Software Development': 82,
        'Data Analytics': 80,
        'Project Management': 75,
        'Information Technology': 70,
        'Networking': 68,
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
            'partner_name': cert.partner_name,
            'last_synced': cert.last_synced,
        })
    
    # Sort by demand score
    recommended.sort(key=lambda x: x['demand_score'], reverse=True)
    return recommended[:20]  # Return top 20 recommendations

@csrf_exempt
def sync_certifications(request):
    """API endpoint to sync certifications from providers using real-time data"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.body else {}
            provider = data.get('provider')
            force = data.get('force', False)
            
            fetcher = CertificationFetcher()
            
            if provider:
                # Sync specific provider
                certifications_data = fetcher.fetch_certifications(provider)
                updated, created = update_certifications_database(certifications_data, provider)
                
                result = {
                    'success': True,
                    'provider': provider,
                    'updated': updated,
                    'created': created,
                    'total': len(certifications_data),
                    'message': f'Successfully synced {provider} certifications'
                }
            else:
                # Sync all providers
                total_updated = 0
                total_created = 0
                providers = ['coursera', 'aws', 'google', 'microsoft', 'cisco']
                
                for prov in providers:
                    try:
                        certifications_data = fetcher.fetch_certifications(prov)
                        updated, created = update_certifications_database(certifications_data, prov)
                        total_updated += updated
                        total_created += created
                    except Exception as e:
                        logger.error(f"Error syncing {prov}: {e}")
                        continue
                
                result = {
                    'success': True,
                    'updated': total_updated,
                    'created': total_created,
                    'message': f'Successfully synced all providers'
                }
            
            return JsonResponse(result)
        except Exception as e:
            logger.error(f"Sync error: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def update_certifications_database(certifications_data, provider):
    """Update database with certification data"""
    updated = 0
    created = 0
    
    for cert_data in certifications_data:
        try:
            cert, created_new = Certification.objects.update_or_create(
                name=cert_data['name'],
                provider=cert_data['provider'],
                defaults={
                    'domain': cert_data.get('domain', 'General'),
                    'description': cert_data.get('description', ''),
                    'rating': cert_data.get('rating', 4.5),
                    'duration': cert_data.get('duration', 'Not specified'),
                    'difficulty_level': cert_data.get('difficulty_level', 'intermediate'),
                    'registration_url': cert_data.get('registration_url', ''),
                    'partner_name': cert_data.get('partner_name', cert_data['provider']),
                    'is_active': cert_data.get('is_active', True),
                    'is_synced': cert_data.get('is_synced', True),
                    'last_updated': timezone.now(),
                    'source': cert_data.get('source', 'realtime')
                }
            )
            
            if created_new:
                created += 1
            else:
                updated += 1
                
        except Exception as e:
            logger.error(f"Error saving certification {cert_data.get('name', 'Unknown')}: {e}")
            continue
    
    return updated, created

def certification_stats(request):
    """Get certification statistics"""
    stats = {
        'total': Certification.objects.filter(is_active=True).count(),
        'active': Certification.objects.filter(is_active=True, is_synced=True).count(),
        'providers': Certification.objects.values('provider').distinct().count(),
        'last_sync': Certification.objects.order_by('-last_updated').first().last_updated.isoformat() if Certification.objects.exists() else None,
        'by_provider': {}
    }
    
    # Add provider-specific stats
    for provider in Certification.objects.values('provider').distinct():
        provider_name = provider['provider']
        stats['by_provider'][provider_name] = {
            'count': Certification.objects.filter(provider=provider_name, is_active=True).count(),
            'synced': Certification.objects.filter(provider=provider_name, is_active=True, is_synced=True).count(),
        }
    
    return JsonResponse(stats)

@csrf_exempt
def clear_cache(request):
    """Clear certification cache and reset sync status"""
    if request.method == 'POST':
        try:
            # Clear all synced certifications
            Certification.objects.update(is_synced=False)
            
            return JsonResponse({
                'success': True, 
                'message': 'Cache cleared successfully. All certifications marked as unsynced.'
            })
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def certification_list(request):
    """Get list of all certifications for API"""
    certifications = Certification.objects.filter(is_active=True)
    
    cert_list = []
    for cert in certifications:
        cert_list.append({
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
            'partner_name': cert.partner_name,
            'is_synced': cert.is_synced,
            'last_updated': cert.last_updated.isoformat() if cert.last_updated else None,
        })
    
    return JsonResponse({'certifications': cert_list})
