import logging
import requests
from django.utils import timezone
from .models import Certification
from .certification_fetchers import CertificationFetcher

logger = logging.getLogger(__name__)

class CertificationSyncManager:
    """Manages certification synchronization from various providers"""
    
    def __init__(self):
        self.fetcher = CertificationFetcher()
        self.providers = ['coursera', 'aws', 'google', 'microsoft', 'cisco']
    
    def sync_all_providers(self, force=False):
        """Sync certifications from all providers"""
        results = {
            'updated': 0,
            'created': 0,
            'errors': 0,
            'details': []
        }
        
        for provider in self.providers:
            try:
                result = self.sync_provider(provider, force)
                results['updated'] += result.get('updated', 0)
                results['created'] += result.get('created', 0)
                results['details'].append({
                    'provider': provider,
                    'updated': result.get('updated', 0),
                    'created': result.get('created', 0)
                })
            except Exception as e:
                logger.error(f"Error syncing {provider}: {e}")
                results['errors'] += 1
                results['details'].append({
                    'provider': provider,
                    'error': str(e)
                })
        
        return results
    
    def sync_provider(self, provider, force=False):
        """Sync certifications from a specific provider"""
        try:
            # Fetch certifications from provider
            certifications = self.fetcher.fetch_certifications(provider)
            
            updated_count = 0
            created_count = 0
            
            for cert_data in certifications:
                cert, created = Certification.objects.update_or_create(
                    name=cert_data['name'],
                    provider=provider,
                    defaults={
                        'domain': cert_data.get('domain', 'General'),
                        'description': cert_data.get('description', ''),
                        'registration_url': cert_data.get('registration_url', ''),
                        'rating': cert_data.get('rating', 4.0),
                        'duration': cert_data.get('duration', 'Varies'),
                        'difficulty_level': cert_data.get('difficulty_level', 'intermediate'),
                        'is_active': cert_data.get('is_active', True),
                        'source': cert_data.get('source', f'{provider}_api'),
                        'last_updated': timezone.now(),
                        'is_synced': True
                    }
                )
                
                if created:
                    created_count += 1
                else:
                    updated_count += 1
            
            return {
                'provider': provider,
                'updated': updated_count,
                'created': created_count,
                'total': updated_count + created_count
            }
            
        except Exception as e:
            logger.error(f"Error in sync_provider for {provider}: {e}")
            raise
