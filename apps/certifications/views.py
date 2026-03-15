from django.shortcuts import render
from django.db.models import Q
from .models import Certification

def certification_list(request):
    search_query = request.GET.get('search', '')
    selected_provider = request.GET.get('provider', '')
    
    certifications = Certification.objects.filter(is_active=True)
    
    if search_query:
        certifications = certifications.filter(
            Q(name__icontains=search_query) |
            Q(domain__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if selected_provider:
        certifications = certifications.filter(provider=selected_provider)
    
    providers = Certification.PROVIDER_CHOICES
    
    context = {
        'certifications': certifications,
        'search_query': search_query,
        'selected_provider': selected_provider,
        'providers': providers,
    }
    
    return render(request, 'certifications/certification_list.html', context)
