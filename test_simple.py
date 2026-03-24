#!/usr/bin/env python
import os
import sys
import django

# Add the project path to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillbridge_careerforge_project.settings')
django.setup()

from django.test import Client
from django.urls import reverse

def test_simple_view():
    """Test a simple view to debug the issue"""
    client = Client()
    
    # Test home page first
    print("Testing home page...")
    response = client.get('/')
    print(f"Home page status: {response.status_code}")
    
    # Test dashboard (which requires login)
    print("\nTesting dashboard...")
    response = client.get('/dashboard/')
    print(f"Dashboard status: {response.status_code}")
    
    # Test internship page
    print("\nTesting internship page...")
    response = client.get('/internship/')
    print(f"Internship page status: {response.status_code}")
    
    if response.status_code == 302:
        print(f"Redirect location: {response.get('Location', 'No Location header')}")
    
    # Test URL resolution
    try:
        url = reverse('core:internship_finder')
        print(f"\nURL resolution successful: {url}")
    except Exception as e:
        print(f"\nURL resolution failed: {e}")

if __name__ == '__main__':
    test_simple_view()
