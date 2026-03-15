from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Avg
from django.http import HttpResponse
import csv
import pandas as pd
from io import StringIO
from .models import Certification
from .serializers import CertificationSerializer

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
    """Sync certifications from external APIs (placeholder)"""
    # This is a placeholder for external API integration
    # You can integrate with actual certification provider APIs here
    
    provider = request.data.get('provider', '')
    
    if provider == 'aws':
        # Example: Call AWS certification API
        # This would require actual API integration
        return Response({
            'message': 'AWS sync not implemented yet',
            'provider': provider
        })
    
    return Response({
        'message': 'External sync functionality',
        'available_providers': ['aws', 'coursera', 'udemy']
    })
