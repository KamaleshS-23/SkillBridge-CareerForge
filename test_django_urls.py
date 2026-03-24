"""
TEST DJANGO URL RESOLUTION
========================

This script tests if Django can resolve the technical test URLs properly.
"""

import os
import sys
import django
from django.conf import settings

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Configure Django settings
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillbridge_careerforge_project.settings')
    django.setup()

try:
    from django.urls import reverse
    from django.test import Client
    from django.contrib.auth.models import User
    
    print("🔧 TESTING DJANGO URL RESOLUTION")
    print("=" * 50)
    
    # Test URL resolution
    try:
        submit_url = reverse('core:submit_technical_test')
        print(f"✅ submit_technical_test URL: {submit_url}")
    except Exception as e:
        print(f"❌ submit_technical_test URL ERROR: {e}")
    
    try:
        results_url = reverse('core:get_technical_test_results')
        print(f"✅ get_technical_test_results URL: {results_url}")
    except Exception as e:
        print(f"❌ get_technical_test_results URL ERROR: {e}")
    
    try:
        aptitude_submit_url = reverse('core:submit_aptitude_test')
        print(f"✅ submit_aptitude_test URL: {aptitude_submit_url}")
    except Exception as e:
        print(f"❌ submit_aptitude_test URL ERROR: {e}")
    
    print()
    print("🎯 EXPECTED URL PATTERNS:")
    print("- /core/api/submit-technical-test/")
    print("- /core/api/technical-test-results/")
    print("- /core/api/submit-aptitude-test/")
    print("- /core/api/aptitude-results/")
    
    print()
    print("🔍 DIAGNOSIS:")
    print("If URLs resolve correctly but still get 404 errors:")
    print("1. Django server needs to be restarted")
    print("2. Functions might not be properly imported")
    print("3. URL patterns might have conflicts")
    
except Exception as e:
    print(f"❌ SETUP ERROR: {e}")
    print("Make sure Django project is properly configured")
