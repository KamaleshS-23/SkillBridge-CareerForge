from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Avg
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
import csv
import pandas as pd
from io import StringIO
from .models import Certification
from .serializers import CertificationSerializer
from .external_apis import CertificationAPIManager, CertificationCache

class CertificationListCreateView(generics.ListCreateAPIView):
    queryset = Certification.objects.filter(is_active=True)
    serializer_class = CertificationSerializer
    
    def get_queryset(self):
        queryset = Certification.objects.filter(is_active=True)
        search = self.request.query_params.get('search', '')
        provider = self.request.query_params.get('provider', '')
        domain = self.request.query_params.get('domain', '')
        difficulty = self.request.query_params.get('difficulty', '')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(domain__icontains=search) |
                Q(description__icontains=search)
            )
        
        if provider:
            queryset = queryset.filter(provider=provider)
        
        if domain:
            queryset = queryset.filter(domain__icontains=domain)
        
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)
            
        return queryset.order_by('-rating', 'name')

class CertificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = [IsAdminUser]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def certification_statistics(request):
    """Get statistics about certifications"""
    stats = {
        'total_certifications': Certification.objects.filter(is_active=True).count(),
        'by_provider': {},
        'by_domain': {},
        'by_difficulty': {},
        'average_rating': Certification.objects.filter(is_active=True).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating'] or 0
    }
    
    # Provider statistics
    for provider_code, provider_name in Certification.PROVIDER_CHOICES:
        count = Certification.objects.filter(provider=provider_code, is_active=True).count()
        if count > 0:
            stats['by_provider'][provider_name] = count
    
    # Domain statistics
    domains = Certification.objects.values_list('domain', flat=True).distinct()
    for domain in domains:
        count = Certification.objects.filter(domain=domain, is_active=True).count()
        if count > 0:
            stats['by_domain'][domain] = count
    
    # Difficulty statistics
    for diff_code, diff_name in Certification.DIFFICULTY_CHOICES:
        count = Certification.objects.filter(difficulty_level=diff_code, is_active=True).count()
        if count > 0:
            stats['by_difficulty'][diff_name] = count
    
    return Response(stats)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def bulk_import_certifications(request):
    """Bulk import certifications from uploaded file"""
    if 'file' not in request.FILES:
        return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['file']
    update_existing = request.data.get('update_existing', False)
    clear_existing = request.data.get('clear_existing', False)
    
    try:
        if clear_existing:
            Certification.objects.all().delete()
        
        # Read file based on type
        if file.name.endswith('.csv'):
            data = []
            decoded_file = file.read().decode('utf-8')
            reader = csv.DictReader(StringIO(decoded_file))
            for row in reader:
                data.append(row)
        elif file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file)
            data = df.to_dict('records')
        else:
            return Response({'error': 'Unsupported file format'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Import data
        imported_count = 0
        updated_count = 0
        error_count = 0
        errors = []
        
        for row in data:
            try:
                from .management.commands.import_certifications import Command
                cmd = Command()
                result = cmd.import_certification(row, update_existing)
                
                if result == 'created':
                    imported_count += 1
                elif result == 'updated':
                    updated_count += 1
                    
            except Exception as e:
                error_count += 1
                errors.append(str(e))
        
        return Response({
            'message': 'Import completed',
            'imported': imported_count,
            'updated': updated_count,
            'errors': error_count,
            'error_details': errors[:10]  # Limit error details
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_certifications(request):
    """Export certifications to CSV"""
    format_type = request.query_params.get('format', 'csv')
    
    if format_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="certifications.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['name', 'provider', 'domain', 'description', 'registration_url', 
                         'rating', 'duration', 'difficulty_level', 'is_active'])
        
        certifications = Certification.objects.all()
        for cert in certifications:
            writer.writerow([
                cert.name, cert.get_provider_display(), cert.domain,
                cert.description, cert.registration_url, cert.rating,
                cert.duration, cert.get_difficulty_level_display(), cert.is_active
            ])
        
        return response
    
    elif format_type == 'excel':
        # Create Excel file
        df = pd.DataFrame(list(Certification.objects.all().values()))
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="certifications.xlsx"'
        
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Certifications')
        
        return response
    
    return Response({'error': 'Unsupported format'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def sync_external_certifications(request):
    """Sync certifications from external APIs"""
    try:
        provider = request.data.get('provider', '')
        force_sync = request.data.get('force', False)
        
        api_manager = CertificationAPIManager()
        cache = CertificationCache()
        
        if not force_sync and cache.is_cache_valid():
            return Response({
                'message': 'Cache is still valid',
                'cache_valid': True,
                'last_updated': Certification.objects.order_by('-last_updated').first().last_updated
            })
        
        if provider:
            # Sync specific provider
            provider_methods = {
                'aws': api_manager.scrape_aws_certifications,
                'google': api_manager.scrape_google_cloud_certifications,
                'microsoft': api_manager.fetch_microsoft_certifications,
                'coursera': api_manager.fetch_coursera_certifications,
                'linkedin': api_manager.fetch_linkedin_certifications
            }
            
            if provider not in provider_methods:
                return Response({
                    'error': f'Unknown provider: {provider}',
                    'available_providers': list(provider_methods.keys())
                }, status=status.HTTP_400_BAD_REQUEST)
            
            certifications = provider_methods[provider]()
        else:
            # Sync all providers
            certifications = api_manager.fetch_all_certifications()
        
        # Update database
        updated_count = 0
        created_count = 0
        
        for cert_data in certifications:
            existing_cert = Certification.objects.filter(
                name=cert_data['name'],
                provider=cert_data['provider']
            ).first()
            
            if existing_cert:
                # Update existing
                for key, value in cert_data.items():
                    if hasattr(existing_cert, key):
                        setattr(existing_cert, key, value)
                existing_cert.save()
                updated_count += 1
            else:
                # Create new
                Certification.objects.create(**cert_data)
                created_count += 1
        
        return Response({
            'message': 'Sync completed successfully',
            'provider': provider or 'all',
            'updated': updated_count,
            'created': created_count,
            'total_fetched': len(certifications),
            'cache_valid': False
        })
        
    except Exception as e:
        return Response({
            'error': str(e),
            'message': 'Sync failed'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def certification_sources(request):
    """Get available certification sources and their status"""
    try:
        sources = []
        
        # Get all certifications grouped by source
        source_stats = {}
        for cert in Certification.objects.all():
            source = cert.source
            if source not in source_stats:
                source_stats[source] = {
                    'count': 0,
                    'last_updated': None,
                    'providers': set()
                }
            source_stats[source]['count'] += 1
            source_stats[source]['providers'].add(cert.provider)
            if cert.last_updated:
                if not source_stats[source]['last_updated'] or cert.last_updated > source_stats[source]['last_updated']:
                    source_stats[source]['last_updated'] = cert.last_updated
        
        # Format response
        for source, stats in source_stats.items():
            sources.append({
                'source': source,
                'count': stats['count'],
                'last_updated': stats['last_updated'],
                'providers': list(stats['providers'])
            })
        
        # Check cache status
        cache = CertificationCache()
        cache_valid = cache.is_cache_valid()
        
        return Response({
            'sources': sources,
            'cache_valid': cache_valid,
            'total_certifications': Certification.objects.count(),
            'active_certifications': Certification.objects.filter(is_active=True).count()
        })
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
