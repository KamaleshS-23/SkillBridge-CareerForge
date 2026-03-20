from django.shortcuts import render
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from .models import Certification
from .external_apis import CertificationAPIManager, CertificationCache
import json

def certification_list(request):
    search_query = request.GET.get('search', '')
    selected_provider = request.GET.get('provider', '')
    selected_domain = request.GET.get('domain', '')
    
    # Fetch data directly from API
    api_manager = CertificationAPIManager()
    all_certifications = api_manager.fetch_all_standard_certifications()
    
    # Convert API data to certification-like objects
    class APICertification:
        def __init__(self, data):
            self.name = data.get('name', '')
            self.provider = data.get('provider', '')
            self.domain = data.get('domain', '')
            self.description = data.get('description', '')
            self.registration_url = data.get('registration_url', '')
            self.rating = data.get('rating', 0.0)
            self.duration = data.get('duration', '')
            self.difficulty_level = data.get('difficulty_level', 'beginner')
            self.source = data.get('source', 'api')
        
        def get_provider_display(self):
            provider_choices = dict(Certification.PROVIDER_CHOICES)
            return provider_choices.get(self.provider, self.provider.title())
        
        def get_difficulty_level_display(self):
            difficulty_choices = dict(Certification.DIFFICULTY_CHOICES)
            return difficulty_choices.get(self.difficulty_level, self.difficulty_level.title())
    
    # Convert API data to objects
    certifications = [APICertification(cert_data) for cert_data in all_certifications]
    
    # Apply filters
    if search_query:
        search_query_lower = search_query.lower()
        certifications = [
            cert for cert in certifications 
            if search_query_lower in cert.name.lower() 
            or search_query_lower in cert.domain.lower() 
            or search_query_lower in cert.description.lower()
        ]
    
    if selected_provider:
        certifications = [cert for cert in certifications if cert.provider == selected_provider]
    
    if selected_domain:
        certifications = [cert for cert in certifications if cert.domain == selected_domain]
    
    providers = Certification.PROVIDER_CHOICES
    
    context = {
        'certifications': certifications,
        'search_query': search_query,
        'selected_provider': selected_provider,
        'selected_domain': selected_domain,
        'providers': providers,
        'api_mode': True,  # Flag to indicate API mode
    }
    
    return render(request, 'certifications/certification_list.html', context)

@staff_member_required
def sync_dashboard(request):
    """Dashboard for managing certification sync operations"""
    
    # Get provider statistics
    provider_stats = []
    providers = Certification.PROVIDER_CHOICES
    
    for provider_code, provider_name in providers:
        count = Certification.objects.filter(provider=provider_code).count()
        last_cert = Certification.objects.filter(provider=provider_code).order_by('-last_updated').first()
        last_updated = last_cert.last_updated if last_cert else None
        
        # Get source for this provider
        sources = Certification.objects.filter(provider=provider_code).values_list('source', flat=True).distinct()
        source = sources[0] if sources else 'manual'
        
        # Determine status
        status = 'inactive'
        if count > 0:
            if last_updated and (timezone.now() - last_updated).days < 7:
                status = 'active'
            else:
                status = 'pending'
        
        provider_stats.append({
            'key': provider_code,
            'name': provider_name,
            'count': count,
            'last_updated': last_updated,
            'source': source,
            'status': status
        })
    
    # Get overall statistics
    total_certifications = Certification.objects.count()
    active_certifications = Certification.objects.filter(is_active=True).count()
    providers_count = len([p for p in provider_stats if p['count'] > 0])
    
    # Get last sync time
    last_sync = Certification.objects.order_by('-last_updated').first()
    last_sync_time = last_sync.last_updated if last_sync else None
    
    context = {
        'providers': provider_stats,
        'total_certifications': total_certifications,
        'active_certifications': active_certifications,
        'providers_count': providers_count,
        'last_sync': last_sync_time.strftime('%H:%M') if last_sync_time else 'Never',
    }
    
    return render(request, 'certifications/sync_dashboard.html', context)
