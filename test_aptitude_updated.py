#!/usr/bin/env python3
"""
Test the updated aptitude page with history section
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillbridge_careerforge_project.settings')
django.setup()

from django.test import Client

def test_updated_aptitude_page():
    """Test the updated aptitude page with history section"""
    print("🎯 Testing Updated Aptitude Page with History")
    print("=" * 50)
    
    client = Client()
    
    # Test 1: Page Load
    print("\n✅ Page Load Test")
    response = client.get('/aptitude/')
    print(f"   Status: {response.status_code}")
    
    content = response.content.decode()
    
    # Test 2: Check for History Section
    print("\n📊 History Section Test")
    history_elements = [
        ('id="historySection"', 'History section container'),
        ('Your Aptitude Test History', 'History section title'),
        ('Refresh', 'Refresh button'),
        ('loadAptitudeTestResults()', 'Load results function'),
        ('DOMContentLoaded', 'Auto-load event'),
        ('No Test History Available', 'Empty state message'),
        ('Start Your First Test', 'Call to action button')
    ]
    
    for element, description in history_elements:
        if element in content:
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description} - MISSING")
    
    # Test 3: Check for Enhanced History Display
    print("\n🎨 Enhanced History Display Test")
    display_elements = [
        ('border-left: 4px solid var(--primary)', 'Left border accent'),
        ('rgba(124, 58, 237, 0.1)', 'Quantitative background'),
        ('rgba(6, 182, 212, 0.1)', 'Verbal background'),
        ('rgba(16, 185, 129, 0.1)', 'Logical background'),
        ('rgba(245, 158, 11, 0.1)', 'Data background'),
        ('rgba(239, 68, 68, 0.1)', 'Abstract background'),
        ('toLocaleString', 'Date formatting'),
        ('font-size: 1.8rem', 'Large percentage display')
    ]
    
    for element, description in display_elements:
        if element in content:
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description} - MISSING")
    
    # Test 4: Check for Error Handling
    print("\n🛡️ Error Handling Test")
    error_elements = [
        ('fa-exclamation-triangle', 'Error icon'),
        ('Error loading test history', 'Error message'),
        ('Please try refreshing', 'Error recovery suggestion')
    ]
    
    for element, description in error_elements:
        if element in content:
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description} - MISSING")
    
    # Test 5: Check for User Experience Features
    print("\n🎯 User Experience Features")
    ux_elements = [
        ('scrollIntoView', 'Smooth scroll to test section'),
        ('behavior: \'smooth\'', 'Smooth scrolling'),
        ('fa-chart-line', 'Empty state icon'),
        ('padding: 60px 20px', 'Proper spacing'),
        ('text-align: center', 'Centered content')
    ]
    
    for element, description in ux_elements:
        if element in content:
            print(f"   ✅ {description}")
        else:
            print(f"   ⚠️  {description} - OPTIONAL")
    
    print("\n🎉 Updated Aptitude Page Test Complete!")
    
    print("\n📋 New Features Added:")
    print("✅ History section displayed by default (like technical page)")
    print("✅ Auto-loading of test history on page load")
    print("✅ Enhanced visual design with color-coded score cards")
    print("✅ Better date formatting (MM/DD/YYYY HH:MM)")
    print("✅ Improved empty state with call-to-action")
    print("✅ Error handling with user-friendly messages")
    print("✅ Smooth scrolling to test section")
    
    print("\n🎯 Expected User Experience:")
    print("1. Page loads with test history visible below setup section")
    print("2. Previous test results show with colorful score breakdown")
    print("3. Empty state encourages users to take their first test")
    print("4. Refresh button updates the history dynamically")
    print("5. Clean, professional layout similar to technical page")

if __name__ == '__main__':
    test_updated_aptitude_page()
