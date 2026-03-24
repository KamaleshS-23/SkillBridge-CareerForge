#!/usr/bin/env python
import os
import sys
import django

# Add to project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillbridge_careerforge_project.settings')
django.setup()

from django.test import Client

def test_api_endpoints():
    """Test internship API endpoints"""
    client = Client()
    
    print("=== Testing API Endpoints ===")
    
    # Test my-internships API
    print("\n1. Testing /api/my-internships/")
    response1 = client.get('/api/my-internships/')
    print(f"   Status: {response1.status_code}")
    if response1.status_code == 200:
        data = response1.json()
        print(f"   Response: {data}")
    else:
        print(f"   Error: {response1.content.decode()}")
    
    # Test internship-stats API
    print("\n2. Testing /api/internship-stats/")
    response2 = client.get('/api/internship-stats/')
    print(f"   Status: {response2.status_code}")
    if response2.status_code == 200:
        data = response2.json()
        print(f"   Response: {data}")
    else:
        print(f"   Error: {response2.content.decode()}")
    
    print("\n=== API Test Complete ===")

if __name__ == '__main__':
    test_api_endpoints()
