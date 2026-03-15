import csv
import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.certifications.models import Certification

class Command(BaseCommand):
    help = 'Import certifications from CSV or Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to CSV or Excel file')
        parser.add_argument('--clear', action='store_true', help='Clear existing data before import')
        parser.add_argument('--update', action='store_true', help='Update existing records')

    def handle(self, *args, **options):
        file_path = options['file_path']
        clear_existing = options['clear']
        update_existing = options['update']

        try:
            if clear_existing:
                with transaction.atomic():
                    Certification.objects.all().delete()
                    self.stdout.write(self.style.WARNING('Cleared all existing certifications'))

            # Determine file type and read data
            if file_path.endswith('.csv'):
                data = self.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                data = self.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format. Use CSV or Excel files.")

            # Import data
            imported_count = 0
            updated_count = 0
            error_count = 0

            with transaction.atomic():
                for row in data:
                    try:
                        result = self.import_certification(row, update_existing)
                        if result == 'created':
                            imported_count += 1
                        elif result == 'updated':
                            updated_count += 1
                    except Exception as e:
                        error_count += 1
                        self.stdout.write(self.style.ERROR(f"Error importing row: {str(e)}"))

            # Summary
            self.stdout.write(self.style.SUCCESS(f'Import completed:'))
            self.stdout.write(f'  - Created: {imported_count} certifications')
            self.stdout.write(f'  - Updated: {updated_count} certifications')
            self.stdout.write(f'  - Errors: {error_count} rows')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Import failed: {str(e)}'))

    def read_csv(self, file_path):
        """Read data from CSV file"""
        data = []
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data

    def read_excel(self, file_path):
        """Read data from Excel file"""
        df = pd.read_excel(file_path)
        return df.to_dict('records')

    def import_certification(self, row, update_existing=False):
        """Import or update a single certification"""
        # Map CSV columns to model fields
        field_mapping = {
            'name': ['name', 'certification_name', 'title'],
            'provider': ['provider', 'platform', 'company'],
            'domain': ['domain', 'category', 'field', 'area'],
            'description': ['description', 'details', 'overview'],
            'registration_url': ['registration_url', 'url', 'link', 'enroll_link'],
            'rating': ['rating', 'score', 'stars'],
            'duration': ['duration', 'length', 'time'],
            'difficulty_level': ['difficulty_level', 'difficulty', 'level']
        }

        # Extract data using flexible field mapping
        cert_data = {}
        for field, possible_keys in field_mapping.items():
            for key in possible_keys:
                if key in row and row[key]:
                    cert_data[field] = str(row[key]).strip()
                    break

        # Validate required fields
        if not cert_data.get('name'):
            raise ValueError("Name is required")

        # Set defaults
        cert_data.setdefault('provider', 'other')
        cert_data.setdefault('rating', 0.0)
        cert_data.setdefault('duration', 'Not specified')
        cert_data.setdefault('difficulty_level', 'beginner')
        cert_data.setdefault('description', 'No description available')

        # Clean and validate data
        cert_data = self.clean_certification_data(cert_data)

        # Check if certification exists
        existing_cert = Certification.objects.filter(
            name__iexact=cert_data['name'],
            provider=cert_data['provider']
        ).first()

        if existing_cert:
            if update_existing:
                for field, value in cert_data.items():
                    setattr(existing_cert, field, value)
                existing_cert.save()
                return 'updated'
            else:
                self.stdout.write(f"Skipping existing certification: {cert_data['name']}")
                return 'skipped'
        else:
            Certification.objects.create(**cert_data)
            return 'created'

    def clean_certification_data(self, data):
        """Clean and validate certification data"""
        # Clean provider
        provider_mapping = {
            'amazon': 'aws',
            'amazon web services': 'aws',
            'infosys limited': 'infosys',
            'tata consultancy services': 'tcs',
            'tcs': 'tcs',
            'coursera': 'coursera',
            'nasscom': 'nasscom',
            'government': 'govt',
            'gov': 'govt',
            'central government': 'govt'
        }
        
        provider = data.get('provider', '').lower()
        data['provider'] = provider_mapping.get(provider, provider)

        # Validate provider choice
        valid_providers = dict(Certification.PROVIDER_CHOICES)
        if data['provider'] not in valid_providers:
            data['provider'] = 'other'

        # Clean rating
        try:
            rating = float(data.get('rating', 0))
            data['rating'] = max(0.0, min(5.0, rating))  # Clamp between 0 and 5
        except (ValueError, TypeError):
            data['rating'] = 0.0

        # Clean difficulty level
        difficulty_mapping = {
            'beginner': 'beginner',
            'basic': 'beginner',
            'entry': 'beginner',
            'intermediate': 'intermediate',
            'mid': 'intermediate',
            'advanced': 'advanced',
            'expert': 'advanced',
            'senior': 'advanced'
        }
        
        difficulty = data.get('difficulty_level', '').lower()
        data['difficulty_level'] = difficulty_mapping.get(difficulty, 'beginner')

        # Validate difficulty choice
        valid_difficulties = dict(Certification.DIFFICULTY_CHOICES)
        if data['difficulty_level'] not in valid_difficulties:
            data['difficulty_level'] = 'beginner'

        # Clean URL
        url = data.get('registration_url', '')
        if url and not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        data['registration_url'] = url

        return data
