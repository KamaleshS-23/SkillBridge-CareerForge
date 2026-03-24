#!/usr/bin/env python
import os
import sys
import django

# Add the project path to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillbridge_careerforge_project.settings')
django.setup()

from django.http import HttpResponse
from django.template import loader

def simple_internship_view(request):
    """Simple test view without authentication"""
    template = loader.get_template('core/internship.html')
    context = {
        'page_title': 'Internship Finder - Test',
        'page_description': 'Test page without database dependencies',
    }
    return HttpResponse(template.render(context, request))
