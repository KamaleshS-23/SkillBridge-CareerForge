from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count, Avg, Q
from apps.certifications.models import Certification
import requests
from urllib.parse import urlparse
import re

class Command(BaseCommand):
    help = 'Validate and clean certification data'

    def add_arguments(self, parser):
        parser.add_argument('--fix', action='store_true', help='Fix issues automatically')
        parser.add_argument('--check-urls', action='store_true', help='Check if URLs are accessible')
        parser.add_argument('--remove-duplicates', action='store_true', help='Remove duplicate certifications')

    def handle(self, *args, **options):
        fix_issues = options['fix']
        check_urls = options['check_urls']
        remove_duplicates = options['remove_duplicates']

        self.stdout.write(self.style.SUCCESS('Starting data validation...'))

        if remove_duplicates:
            self.remove_duplicates(fix_issues)

        self.validate_certifications(fix_issues)

        if check_urls:
            self.check_urls(fix_issues)

        self.stdout.write(self.style.SUCCESS('Data validation completed!'))

    def validate_certifications(self, fix_issues=False):
        """Validate certification data"""
        self.stdout.write('Validating certifications...')
        
        certifications = Certification.objects.all()
        issues_found = 0
        issues_fixed = 0

        for cert in certifications:
            cert_issues = []

            # Check required fields
            if not cert.name or cert.name.strip() == '':
                cert_issues.append('Missing name')
            
            if not cert.domain or cert.domain.strip() == '':
                cert_issues.append('Missing domain')
            
            # Validate rating
            if cert.rating < 0 or cert.rating > 5:
                cert_issues.append(f'Invalid rating: {cert.rating}')
                if fix_issues:
                    cert.rating = max(0, min(5, cert.rating))
                    issues_fixed += 1
            
            # Validate URL
            if cert.registration_url:
                parsed_url = urlparse(cert.registration_url)
                if not parsed_url.scheme or not parsed_url.netloc:
                    cert_issues.append('Invalid URL format')
                    if fix_issues:
                        if not cert.registration_url.startswith(('http://', 'https://')):
                            cert.registration_url = 'https://' + cert.registration_url
                            issues_fixed += 1
            
            # Validate provider
            valid_providers = dict(Certification.PROVIDER_CHOICES)
            if cert.provider not in valid_providers:
                cert_issues.append(f'Invalid provider: {cert.provider}')
                if fix_issues:
                    cert.provider = 'other'
                    issues_fixed += 1
            
            # Validate difficulty
            valid_difficulties = dict(Certification.DIFFICULTY_CHOICES)
            if cert.difficulty_level not in valid_difficulties:
                cert_issues.append(f'Invalid difficulty: {cert.difficulty_level}')
                if fix_issues:
                    cert.difficulty_level = 'beginner'
                    issues_fixed += 1
            
            # Clean description
            if cert.description:
                # Remove excessive whitespace
                cert.description = re.sub(r'\s+', ' ', cert.description).strip()
                
                # Check for very short descriptions
                if len(cert.description) < 10:
                    cert_issues.append('Description too short')
                    if fix_issues:
                        cert.description = 'No detailed description available.'
                        issues_fixed += 1
            
            # Save fixes
            if cert_issues and fix_issues:
                cert.save()
            
            if cert_issues:
                issues_found += len(cert_issues)
                self.stdout.write(f"  Issues with '{cert.name}': {', '.join(cert_issues)}")

        self.stdout.write(f'Found {issues_found} issues. Fixed {issues_fixed} issues.')

    def check_urls(self, fix_issues=False):
        """Check if certification URLs are accessible"""
        self.stdout.write('Checking URL accessibility...')
        
        certifications = Certification.objects.filter(registration_url__isnull=False).exclude(registration_url='')
        
        for cert in certifications:
            try:
                response = requests.head(cert.registration_url, timeout=10, allow_redirects=True)
                if response.status_code >= 400:
                    self.stdout.write(f"  URL error for '{cert.name}': HTTP {response.status_code}")
                    if fix_issues:
                        cert.is_active = False
                        cert.save()
                        self.stdout.write(f"    Deactivated certification due to broken URL")
                else:
                    self.stdout.write(f"  ✓ {cert.name} - URL OK")
            except requests.RequestException as e:
                self.stdout.write(f"  URL check failed for '{cert.name}': {str(e)}")
                if fix_issues:
                    cert.is_active = False
                    cert.save()
                    self.stdout.write(f"    Deactivated certification due to URL error")

    def remove_duplicates(self, fix_issues=False):
        """Remove duplicate certifications"""
        self.stdout.write('Checking for duplicates...')
        
        # Find duplicates based on name and provider
        duplicates = Certification.objects.values('name', 'provider').annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        total_duplicates = 0
        for dup in duplicates:
            certs = Certification.objects.filter(name=dup['name'], provider=dup['provider']).order_by('id')
            duplicate_count = certs.count() - 1
            total_duplicates += duplicate_count
            
            self.stdout.write(f"  Found {duplicate_count + 1} duplicates for '{dup['name']}' ({dup['provider']})")
            
            if fix_issues:
                # Keep the first one, delete the rest
                for cert in certs[1:]:
                    cert.delete()
                    self.stdout.write(f"    Deleted duplicate: {cert.id}")
        
        self.stdout.write(f'Found {total_duplicates} duplicate certifications.')
        if fix_issues:
            self.stdout.write(f'All duplicates have been removed.')

    def generate_data_report(self):
        """Generate a comprehensive data quality report"""
        self.stdout.write('Generating data quality report...')
        
        total_certs = Certification.objects.count()
        active_certs = Certification.objects.filter(is_active=True).count()
        
        # Provider distribution
        provider_stats = {}
        for provider_code, provider_name in Certification.PROVIDER_CHOICES:
            count = Certification.objects.filter(provider=provider_code).count()
            if count > 0:
                provider_stats[provider_name] = count
        
        # Domain distribution
        domain_stats = {}
        domains = Certification.objects.values_list('domain', flat=True).distinct()
        for domain in domains:
            count = Certification.objects.filter(domain=domain).count()
            domain_stats[domain] = count
        
        # Quality metrics
        missing_descriptions = Certification.objects.filter(
            Q(description__isnull=True) | 
            Q(description='') |
            Q(description__exact='No description available')
        ).count()
        
        invalid_urls = Certification.objects.filter(
            registration_url__isnull=False
        ).exclude(
            registration_url__regex=r'^https?://'
        ).count()
        
        report = f"""
=== CERTIFICATION DATA QUALITY REPORT ===
Total Certifications: {total_certs}
Active Certifications: {active_certs}
Inactive Certifications: {total_certs - active_certs}

PROVIDER DISTRIBUTION:
{chr(10).join([f"  {name}: {count}" for name, count in provider_stats.items()])}

DOMAIN DISTRIBUTION:
{chr(10).join([f"  {domain}: {count}" for domain, count in domain_stats.items()])}

QUALITY ISSUES:
  Missing Descriptions: {missing_descriptions}
  Invalid URLs: {invalid_urls}
  Average Rating: {Certification.objects.aggregate(avg_rating=Avg('rating'))['avg_rating']:.2f}
        """
        
        self.stdout.write(report)
