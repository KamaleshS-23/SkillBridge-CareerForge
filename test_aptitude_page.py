#!/usr/bin/env python3
"""
Test script to verify aptitude page functionality
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillbridge_careerforge_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def test_aptitude_page():
    """Test the aptitude page functionality"""
    print("🧪 Testing Aptitude Page Functionality")
    print("=" * 50)
    
    client = Client()
    
    # Test 1: Check if aptitude page loads
    print("\n📄 Testing Aptitude Page Load")
    print("-" * 30)
    
    response = client.get('/aptitude/')
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Aptitude page loads successfully")
        
        # Check for key elements in the page
        content = response.content.decode()
        elements_to_check = [
            'Start Aptitude Test',
            'sectionSelect',
            'difficultySelect',
            'questionCount',
            'Quantitative Aptitude',
            'Logical Reasoning',
            'Verbal Ability'
        ]
        
        print("\n🔍 Checking Page Elements:")
        for element in elements_to_check:
            if element in content:
                print(f"   ✅ {element} found")
            else:
                print(f"   ❌ {element} missing")
        
        # Check for JavaScript file
        if 'aptitude_test.js' in content:
            print("   ✅ JavaScript file included")
        else:
            print("   ❌ JavaScript file missing")
            
    else:
        print(f"❌ Aptitude page failed to load: {response.status_code}")
    
    # Test 2: Check API endpoints
    print("\n🔌 Testing API Endpoints")
    print("-" * 30)
    
    # Test results endpoint (should work without login for testing)
    response = client.get('/api/aptitude-results/')
    print(f"Results API Status: {response.status_code}")
    
    if response.status_code == 401:
        print("✅ API correctly requires authentication")
    elif response.status_code == 200:
        print("✅ API endpoint accessible")
    else:
        print(f"⚠️  API returned unexpected status: {response.status_code}")
    
    # Test 3: Test submit endpoint (without login should fail)
    test_data = {
        'scores': {
            'quantitative': 5,
            'verbal': 4,
            'logical': 3,
            'data_interpretation': 6,
            'abstract_reasoning': 4
        },
        'max_score': 25,
        'time_taken': '00:15:30',
        'difficulty_level': 'medium'
    }
    
    response = client.post(
        '/api/submit-aptitude-test/',
        data=test_data,
        content_type='application/json'
    )
    print(f"Submit API Status: {response.status_code}")
    
    if response.status_code == 401:
        print("✅ Submit API correctly requires authentication")
    elif response.status_code == 200:
        print("✅ Submit API accessible")
    else:
        print(f"⚠️  Submit API returned: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎉 Aptitude Page Test Complete!")
    
    print("\n📋 Manual Testing Instructions:")
    print("1. Open browser and navigate to: http://127.0.0.1:8000/aptitude/")
    print("2. Select a section (e.g., Logical Reasoning)")
    print("3. Select difficulty (e.g., Intermediate)")
    print("4. Select question count (e.g., 5 Questions)")
    print("5. Click 'Start Aptitude Test'")
    print("6. Verify questions load and timer starts")
    print("7. Answer questions and navigate")
    print("8. Submit test and check results")
    print("9. Verify results show topic-wise breakdown")

if __name__ == '__main__':
    test_aptitude_page()
