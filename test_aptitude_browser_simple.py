#!/usr/bin/env python3
"""
Simple browser test for aptitude page
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillbridge_careerforge_project.settings')
django.setup()

from django.test import Client

def test_aptitude_browser():
    """Test aptitude page in browser-like environment"""
    print("🌐 Testing Aptitude Page in Browser")
    print("=" * 40)
    
    client = Client()
    
    # Load the page
    response = client.get('/aptitude/')
    print(f"✅ Page Status: {response.status_code}")
    
    content = response.content.decode()
    
    # Check for clean HTML structure
    checks = [
        ('<!DOCTYPE html>', 'Proper HTML5 doctype'),
        ('id="setupSection"', 'Setup section'),
        ('id="testSection"', 'Test section'),
        ('id="resultsSection"', 'Results section'),
        ('id="sectionSelect"', 'Section dropdown'),
        ('id="difficultySelect"', 'Difficulty dropdown'),
        ('id="questionCount"', 'Question count'),
        ('id="startTestBtn"', 'Start button'),
        ('Quantitative Aptitude', 'Quantitative section'),
        ('Verbal Ability', 'Verbal section'),
        ('Logical Reasoning', 'Logical section'),
        ('Data Interpretation', 'Data section'),
        ('Abstract Reasoning', 'Abstract section'),
        ('aptitude_test.js', 'JavaScript file'),
        ('🧠 Aptitude test page loaded', 'Console log'),
        ('function viewHistory', 'History function'),
        ('function loadAptitudeTestResults', 'Load results function')
    ]
    
    print("\n🔍 Checking Page Elements:")
    for check, description in checks:
        if check in content:
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description} - MISSING")
    
    # Check for unwanted CSS remnants
    unwanted = [
        'box-shadow: 0 14px 30px rgba',
        '@media (max-width: 768px)',
        '.grid-2',
        'label { display: block'
    ]
    
    print("\n🧹 Checking for Unwanted Code:")
    for item in unwanted:
        if item in content:
            print(f"   ⚠️  Found unwanted: {item}")
        else:
            print(f"   ✅ Clean: {item}")
    
    print("\n🎉 Browser Test Complete!")
    print("\n📋 Expected Console Output:")
    print("   🧠 Aptitude test page loaded")
    print("   ✅ Loaded XX sample questions")
    print("   ✅ Event listeners attached")
    
    print("\n🎯 Next Steps:")
    print("1. Open http://127.0.0.1:8000/aptitude/")
    print("2. Select any section, difficulty, and question count")
    print("3. Click 'Start Aptitude Test'")
    print("4. Verify test functionality")

if __name__ == '__main__':
    test_aptitude_browser()
