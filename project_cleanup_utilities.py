#!/usr/bin/env python3
"""
PROJECT CLEANUP UTILITIES
========================
Consolidated utility functions for testing, debugging, and maintenance.
This file consolidates all the scattered test and debug scripts into one organized location.
"""

import os
import sys
import django
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillbridge_careerforge_project.settings')
django.setup()

from django.test import Client
from django.template import loader
from django.contrib.auth import get_user_model
from django.db import connection

User = get_user_model()

class ProjectTester:
    """Main testing and debugging utilities"""
    
    def __init__(self):
        self.client = Client()
        self.test_results = {}
    
    def test_ai_mock_interview(self):
        """Test AI Mock Interview Integration"""
        print("🤖 Testing AI Mock Interview Integration")
        print("=" * 50)
        
        dashboard_path = 'skillbridge_careerforge_project/templates/core/dashboard.html'
        
        if not os.path.exists(dashboard_path):
            print("❌ dashboard.html not found")
            return False
        
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = {
            'loadAIMockInterviewPage': 'loadAIMockInterviewPage()' in content,
            'ai_mock_container': 'ai-mock-interview-container' in content,
            'selectType_function': 'function selectType(' in content,
            'selectDifficulty_function': 'function selectDifficulty(' in content,
            'startInterview_function': 'function startInterview()' in content,
            'sendAnswer_function': 'function sendAnswer()' in content,
            'closeAIMockInterview_function': 'function closeAIMockInterview()' in content,
            'timer_functionality': 'startTimer()' in content and 'updateTimerDisplay()' in content,
            'question_system': 'getFirstQuestion(' in content,
            'chat_functionality': 'addMessage(' in content and 'getElementById("chat")' in content,
            'proper_html_structure': '<div class="ai-mock-interview-container">' in content,
        }
        
        button_ids = ['btn-hr', 'btn-technical', 'btn-communication']
        missing_buttons = [btn_id for btn_id in button_ids if f'id="{btn_id}"' not in content]
        
        element_ids = ['home', 'interview', 'chat', 'answer-input', 'timer-display']
        missing_elements = [elem_id for elem_id in element_ids if f'getElementById("{elem_id}")' not in content]
        
        all_passed = True
        for check_name, result in checks.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {status} {check_name}")
            if not result:
                all_passed = False
        
        if missing_buttons:
            print(f"⚠️  MISSING BUTTON IDs: {', '.join(missing_buttons)}")
            all_passed = False
        
        if missing_elements:
            print(f"⚠️  MISSING ELEMENT IDs: {', '.join(missing_elements)}")
            all_passed = False
        
        self.test_results['ai_mock_interview'] = all_passed
        return all_passed
    
    def test_aptitude_browser_functionality(self):
        """Test the aptitude page with browser-like interactions"""
        print("\n🌐 Testing Aptitude Page Browser Functionality")
        print("=" * 50)
        
        response = self.client.get('/aptitude/')
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Page loads successfully")
            
            content = response.content.decode()
            
            # JavaScript checks
            js_checks = {
                'currentTest variable': 'currentTest' in content,
                'IIFE wrapping': '(function()' in content,
                'JS file included': 'aptitude_test.js' in content,
            }
            
            for check_name, result in js_checks.items():
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"   {status} {check_name}")
            
            # Form elements
            form_elements = [
                'sectionSelect', 'difficultySelect', 'questionCount', 'startTestBtn'
            ]
            
            print("\n🔍 Checking Form Elements")
            for element in form_elements:
                if f'id="{element}"' in content:
                    print(f"   ✅ {element} found")
                else:
                    print(f"   ❌ {element} missing")
            
            # Test sections
            sections = [
                'Quantitative Aptitude', 'Verbal Ability', 'Logical Reasoning',
                'Data Interpretation', 'Abstract Reasoning'
            ]
            
            print("\n📚 Checking Test Sections")
            for section in sections:
                if section in content:
                    print(f"   ✅ {section} available")
                else:
                    print(f"   ❌ {section} missing")
            
            self.test_results['aptitude_browser'] = True
            return True
        else:
            print(f"❌ Page failed to load: {response.status_code}")
            self.test_results['aptitude_browser'] = False
            return False
    
    def test_internship_page(self):
        """Debug the internship page by checking template rendering"""
        print("\n🎯 Testing Internship Page")
        print("=" * 30)
        
        try:
            response = self.client.get('/internship/')
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Internship page loads successfully!")
                
                template = loader.get_template('core/internship.html')
                context = {
                    'page_title': 'Internship Finder',
                    'page_description': 'Search internships across top companies worldwide',
                }
                
                try:
                    rendered = template.render(context)
                    print("✅ Template renders successfully!")
                    print(f"Template length: {len(rendered)} characters")
                    
                    sections = [
                        'My Internship Journey',
                        'Internship Statistics', 
                        'Available Internships'
                    ]
                    
                    for section in sections:
                        if section in rendered:
                            print(f"✅ {section} section found")
                        else:
                            print(f"❌ {section} section missing")
                    
                    self.test_results['internship_page'] = True
                    return True
                    
                except Exception as e:
                    print(f"❌ Template rendering error: {str(e)}")
                    self.test_results['internship_page'] = False
                    return False
            else:
                print(f"❌ Error loading page. Status: {response.status_code}")
                self.test_results['internship_page'] = False
                return False
                
        except Exception as e:
            print(f"❌ Exception occurred: {str(e)}")
            self.test_results['internship_page'] = False
            return False
    
    def test_database_connectivity(self):
        """Test database connectivity and show tables"""
        print("\n🗄️ Testing Database Connectivity")
        print("=" * 35)
        
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            print(f"✅ Database connected successfully!")
            print(f"📊 Found {len(tables)} tables:")
            
            for table in sorted([table[0] for table in tables]):
                print(f"   - {table}")
            
            self.test_results['database'] = True
            return True
            
        except Exception as e:
            print(f"❌ Database connection failed: {str(e)}")
            self.test_results['database'] = False
            return False
    
    def test_api_endpoints(self):
        """Test basic API endpoints"""
        print("\n🔌 Testing API Endpoints")
        print("=" * 25)
        
        endpoints = [
            ('/', 'Home Page'),
            ('/accounts/login/', 'Login Page'),
            ('/skills/', 'Skills Page'),
            ('/jobs/', 'Jobs Page'),
        ]
        
        all_passed = True
        for endpoint, name in endpoints:
            try:
                response = self.client.get(endpoint)
                status = "✅ PASS" if response.status_code in [200, 302] else "❌ FAIL"
                print(f"  {status} {name}: {response.status_code}")
                if response.status_code not in [200, 302]:
                    all_passed = False
            except Exception as e:
                print(f"  ❌ FAIL {name}: {str(e)}")
                all_passed = False
        
        self.test_results['api_endpoints'] = all_passed
        return all_passed
    
    def run_all_tests(self):
        """Run all available tests"""
        print("🚀 RUNNING COMPLETE PROJECT TEST SUITE")
        print("=" * 50)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run all tests
        self.test_database_connectivity()
        self.test_api_endpoints()
        self.test_ai_mock_interview()
        self.test_aptitude_browser_functionality()
        self.test_internship_page()
        
        # Summary
        print("\n" + "=" * 50)
        print("📋 TEST SUMMARY")
        print("=" * 50)
        
        passed = 0
        total = len(self.test_results)
        
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {status} {test_name}")
            if result:
                passed += 1
        
        print(f"\n📊 RESULTS: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Project is in good shape.")
        else:
            print("⚠️  Some tests failed. Review the issues above.")
        
        return passed == total

class DatabaseUtilities:
    """Database maintenance and checking utilities"""
    
    @staticmethod
    def show_tables():
        """Show all database tables"""
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Database Tables:")
        for table in sorted([table[0] for table in tables]):
            print(f"  - {table}")
        return [table[0] for table in tables]
    
    @staticmethod
    def check_table_structure(table_name):
        """Check structure of a specific table"""
        cursor = connection.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        print(f"\nStructure of {table_name}:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        return columns

def main():
    """Main interface for utilities"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Project Cleanup and Testing Utilities')
    parser.add_argument('--test', action='store_true', help='Run all tests')
    parser.add_argument('--db-show', action='store_true', help='Show database tables')
    parser.add_argument('--db-check', type=str, help='Check specific table structure')
    
    args = parser.parse_args()
    
    if args.test:
        tester = ProjectTester()
        tester.run_all_tests()
    elif args.db_show:
        DatabaseUtilities.show_tables()
    elif args.db_check:
        DatabaseUtilities.check_table_structure(args.db_check)
    else:
        print("Project Cleanup Utilities")
        print("Usage:")
        print("  python project_cleanup_utilities.py --test")
        print("  python project_cleanup_utilities.py --db-show")
        print("  python project_cleanup_utilities.py --db-check <table_name>")
if __name__ == '__main__':
    main()
