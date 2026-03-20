# Certification API Integration

This document explains how to use the API integration system for fetching certifications from external providers.

## 🌐 Supported Providers

### API-Based Providers
- **Microsoft Learn Catalog API** - Official API access
- **Coursera API** - Limited public access
- **LinkedIn Learning API** - Requires special access

### Web Scraping Providers
- **AWS Certifications** - Scraped from official website
- **Google Cloud Certifications** - Scraped from official website

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install requests beautifulsoup4 lxml
```

### 2. Sync All Providers
```bash
# Management command
python manage.py sync_certifications

# Sync specific provider
python manage.py sync_certifications --provider aws

# Force sync (ignore cache)
python manage.py sync_certifications --force

# Dry run (show what would be synced)
python manage.py sync_certifications --dry-run
```

### 3. Use API Endpoints
```bash
# Sync via API
POST /api/certifications/sync/
{
    "provider": "aws",
    "force": true
}

# Get sources status
GET /api/certifications/sources/

# Get all certifications
GET /api/certifications/
```

### 4. Access Sync Dashboard
Visit: `/certifications/sync/` (admin access required)

## 📊 API Integration Details

### Microsoft Learn Catalog API
- **Endpoint**: `https://learn.microsoft.com/api/catalog/`
- **Authentication**: None (public API)
- **Rate Limit**: None documented
- **Data**: Courses, modules, certifications

### Coursera API
- **Endpoint**: `https://api.coursera.org/api/courses.v1`
- **Authentication**: None (limited public access)
- **Rate Limit**: May exist
- **Data**: Course information, partners

### AWS Web Scraping
- **URL**: `https://aws.amazon.com/certification/`
- **Method**: BeautifulSoup scraping
- **Frequency**: Respectful (1 second delay)
- **Data**: Certification names, descriptions, links

### Google Cloud Web Scraping
- **URL**: `https://cloud.google.com/certification`
- **Method**: BeautifulSoup scraping
- **Frequency**: Respectful (1 second delay)
- **Data**: Certification names, descriptions, links

## 🔧 Configuration

### Cache Settings
```python
# In external_apis.py
class CertificationCache:
    def __init__(self):
        self.cache_timeout = 24  # hours
```

### Provider Settings
```python
# Add new providers in PROVIDER_CHOICES
PROVIDER_CHOICES = [
    ('aws', 'AWS'),
    ('google', 'Google Cloud'),
    ('microsoft', 'Microsoft'),
    # ... add more providers
]
```

## 📱 Usage Examples

### Python Script
```python
from apps.certifications.external_apis import CertificationAPIManager

# Initialize API manager
api_manager = CertificationAPIManager()

# Fetch all certifications
certifications = api_manager.fetch_all_certifications()

# Update database
updated, created = api_manager.update_certifications_database()
print(f"Updated: {updated}, Created: {created}")
```

### API Call
```python
import requests

# Sync AWS certifications
response = requests.post(
    'http://localhost:8000/api/certifications/sync/',
    json={'provider': 'aws'},
    headers={'Authorization': 'Bearer your-token'}
)
```

## 🔄 Sync Schedule

### Automatic Sync (Recommended)
```python
# In settings.py
CELERY_BEAT_SCHEDULE = {
    'sync-certifications': {
        'task': 'apps.certifications.tasks.sync_certifications',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
}
```

### Manual Sync
- Use management commands
- Use sync dashboard
- Use API endpoints

## 🛡️ Rate Limiting & Best Practices

### Respectful Scraping
- 1-second delay between requests
- Use appropriate User-Agent
- Don't overload servers

### API Usage
- Check rate limits
- Handle errors gracefully
- Use caching when possible

### Error Handling
- Network timeouts
- API changes
- HTML structure changes

## 📈 Monitoring

### Sync Dashboard Features
- Provider status
- Last sync times
- Certification counts
- Sync logs

### API Monitoring
- Response times
- Error rates
- Success rates

## 🔍 Troubleshooting

### Common Issues
1. **Network timeouts** - Check internet connection
2. **API changes** - Update scraping logic
3. **Rate limits** - Implement delays
4. **HTML changes** - Update selectors

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Future Enhancements

### Planned Providers
- edX
- Udacity
- Pluralsight
- LinkedIn Learning (full API)

### Features
- Real-time sync
- Webhook support
- Advanced filtering
- Analytics dashboard

## 📞 Support

For questions or issues:
1. Check sync logs
2. Review API documentation
3. Test with dry-run mode
4. Contact development team

## 🔐 Security Notes

- API credentials stored securely
- Rate limiting implemented
- Input validation on all endpoints
- Admin access required for sync dashboard
