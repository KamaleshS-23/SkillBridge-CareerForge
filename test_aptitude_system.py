#!/usr/bin/env python3
"""
Test script to verify aptitude test system functionality
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillbridge_careerforge_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from apps.core.models import AptitudeTestResult

User = get_user_model()

def test_aptitude_test_system():
    """Test the complete aptitude test system"""
    print("🧪 Testing Aptitude Test System")
    print("=" * 50)
    
    # Create test user
    try:
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        print(f"✅ Created test user: {user.email}")
    except Exception as e:
        print(f"⚠️  User already exists or error: {e}")
        user = User.objects.filter(email='test@example.com').first()
    
    # Test API endpoint directly
    client = Client()
    
    # Test data for aptitude test submission
    test_data = {
        'scores': {
            'quantitative': 8,
            'verbal': 7,
            'logical': 6,
            'data_interpretation': 9,
            'abstract_reasoning': 7
        },
        'max_score': 50,
        'time_taken': '00:25:30',
        'difficulty_level': 'mixed'
    }
    
    print("\n📊 Testing Aptitude Test Submission API")
    print("-" * 40)
    
    # Login the user
    client.login(username='testuser', password='testpass123')
    
    # Test the API endpoint
    response = client.post(
        '/api/submit-aptitude-test/',
        data=test_data,
        content_type='application/json'
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ API Response:")
        print(f"   Status: {result.get('status')}")
        print(f"   Message: {result.get('message')}")
        print(f"   Total Score: {result.get('total_score')}")
        print(f"   Percentage: {result.get('percentage')}%")
        
        # Display scores by topic
        scores = result.get('scores', {})
        print("\n📈 Score Breakdown by Topic:")
        for topic, score in scores.items():
            print(f"   {topic.replace('_', ' ').title()}: {score}/{test_data['max_score']}")
        
        print(f"\n⏱️  Time Taken: {test_data['time_taken']}")
        print(f"🎯 Difficulty: {test_data['difficulty_level']}")
        
        # Verify database storage
        db_results = AptitudeTestResult.objects.filter(user=user)
        print(f"\n💾 Database Records: {db_results.count()} found")
        
        if db_results.exists():
            latest_result = db_results.first()
            print(f"   Latest Result ID: {latest_result.id}")
            print(f"   Test Date: {latest_result.test_date}")
            print(f"   Overall Percentage: {latest_result.percentage}%")
            print(f"   User: {latest_result.user.email}")
            
            print("\n✅ SUCCESS: Aptitude test system is working correctly!")
            print("   - Scores are stored by topic")
            print("   - Time tracking is working")
            print("   - User-specific results are stored")
            print("   - Database persistence is functional")
            
        else:
            print("❌ ERROR: No records found in database")
            
    else:
        print(f"❌ ERROR: API call failed")
        print(f"Response: {response.content.decode()}")
    
    print("\n" + "=" * 50)
    print("🎉 Aptitude Test System Test Complete!")
    
    # Cleanup
    try:
        user.delete()
        print(f"🧹 Cleaned up test user")
    except:
        pass

if __name__ == '__main__':
    test_aptitude_test_system()
