"""
Management command to sync certifications from external APIs
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.certifications.external_apis import CertificationAPIManager, CertificationCache
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sync certifications from external APIs and update database'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force sync even if cache is valid'
        )
        parser.add_argument(
            '--provider',
            type=str,
            help='Sync only specific provider (aws, google, microsoft, coursera, government)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be synced without actually updating'
        )
    
    def handle(self, *args, **options):
        force_sync = options.get('force', False)
        specific_provider = options.get('provider', '')
        dry_run = options.get('dry_run', False)
        
        self.stdout.write('Starting certification sync...')
        
        # Check cache
        cache = CertificationCache()
        if not force_sync and cache.is_cache_valid():
            self.stdout.write(
                self.style.WARNING('Cache is valid. Use --force to sync anyway.')
            )
            return
        
        # Initialize API manager
        api_manager = CertificationAPIManager()
        
        if specific_provider:
            self.stdout.write(f'Syncing {specific_provider} certifications...')
            certifications = self._sync_provider(api_manager, specific_provider)
        else:
            self.stdout.write('Syncing all standard providers...')
            certifications = api_manager.fetch_all_standard_certifications()
        
        if dry_run:
            self.stdout.write(f'DRY RUN: Would sync {len(certifications)} certifications:')
            for cert in certifications[:5]:  # Show first 5
                self.stdout.write(f'  - {cert.get("name", "Unknown")} ({cert.get("provider", "Unknown")})')
            if len(certifications) > 5:
                self.stdout.write(f'  ... and {len(certifications) - 5} more')
        else:
            updated, created = api_manager.update_certifications_database()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Sync completed: {updated} updated, {created} created'
                )
            )
    
    def _sync_provider(self, api_manager, provider):
        """Sync certifications from a specific provider"""
        provider_methods = {
            'aws': api_manager.scrape_aws_certifications,
            'google': api_manager.scrape_google_cloud_certifications,
            'microsoft': api_manager.fetch_microsoft_certifications,
            'coursera': api_manager.fetch_coursera_standard_certifications,
            'government': api_manager.fetch_government_certifications,
            'nasscom': api_manager.fetch_government_certifications,
            'govt': api_manager.fetch_government_certifications
        }
        
        if provider not in provider_methods:
            self.stdout.write(
                self.style.ERROR(f'Unknown provider: {provider}')
            )
            return []
        
        try:
            return provider_methods[provider]()
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error syncing {provider}: {e}')
            )
            return []
