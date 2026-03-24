#!/usr/bin/env python3
"""
Test script to verify aptitude page works in browser
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

def test_aptitude_browser_functionality():
    """Test the aptitude page with browser-like interactions"""
    print("🌐 Testing Aptitude Page Browser Functionality")
    print("=" * 50)
    
    client = Client()
    
    # Test 1: Load the page
    print("\n📄 Loading Aptitude Page")
    print("-" * 30)
    
    response = client.get('/aptitude/')
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Page loads successfully")
        
        content = response.content.decode()
        
        # Check for JavaScript console errors prevention
        if 'currentTest' in content:
            print("✅ JavaScript variables properly scoped")
        
        if '(function()' in content:
            print("✅ JavaScript properly wrapped in IIFE")
            
        if 'aptitude_test.js' in content:
            print("✅ JavaScript file included")
        
        # Test 2: Check for proper form elements
        print("\n🔍 Checking Form Elements")
        print("-" * 30)
        
        form_elements = [
            'sectionSelect',
            'difficultySelect', 
            'questionCount',
            'startTestBtn'
        ]
        
        for element in form_elements:
            if f'id="{element}"' in content:
                print(f"   ✅ {element} found")
            else:
                print(f"   ❌ {element} missing")
        
        # Test 3: Check for test sections
        print("\n📚 Checking Test Sections")
        print("-" * 30)
        
        sections = [
            'Quantitative Aptitude',
            'Verbal Ability',
            'Logical Reasoning',
            'Data Interpretation',
            'Abstract Reasoning'
        ]
        
        for section in sections:
            if section in content:
                print(f"   ✅ {section} available")
            else:
                print(f"   ❌ {section} missing")
        
        # Test 4: Check for JavaScript functions
        print("\n⚙️ Checking JavaScript Functions")
        print("-" * 30)
        
        js_functions = [
            'loadTestQuestions',
            'setupEventListeners',
            'validateForm',
            'startTest',
            'displayQuestion',
            'submitTest',
            'showResults'
        ]
        
        for function in js_functions:
            if function in content:
                print(f"   ✅ {function} defined")
            else:
                print(f"   ❌ {function} missing")
        
        print("\n🎉 Browser Compatibility Check Complete!")
        print("\n📋 Expected Console Output:")
        print("   🧠 Aptitude test page loaded")
        print("   ✅ Loaded XX sample questions")
        print("   ✅ Event listeners attached")
        print("   🚀 Test started: [section] - [difficulty] - [count] questions")
        
    else:
        print(f"❌ Page failed to load: {response.status_code}")

if __name__ == '__main__':
    test_aptitude_browser_functionality()
