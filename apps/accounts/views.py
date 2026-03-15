from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Certification
from .forms import CertificationForm


@login_required
def profile(request):
    certifications = request.user.certifications.all()

    # 🔹 Recommended certifications based on interest
    recommended = []

    if request.user.field_of_interest == 'data_science':
        recommended = [
            {'name': 'Data Science with Python', 'org': 'Infosys Springboard'},
            {'name': 'Machine Learning Basics', 'org': 'AICTE'},
        ]
    elif request.user.field_of_interest == 'web_dev':
        recommended = [
            {'name': 'Full Stack Web Development', 'org': 'Internshala'},
            {'name': 'Frontend Development', 'org': 'Edunet Foundation'},
        ]
    elif request.user.field_of_interest == 'ai_ml':
        recommended = [
            {'name': 'Artificial Intelligence', 'org': 'Infosys'},
            {'name': 'Deep Learning Fundamentals', 'org': 'AICTE'},
        ]

    context = {
        'certifications': certifications,
        'recommended': recommended,
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def add_certification(request):
    if request.method == 'POST':
        form = CertificationForm(request.POST)
        if form.is_valid():
            cert = form.save(commit=False)
            cert.user = request.user
            cert.save()
            return redirect('profile')
    else:
        form = CertificationForm()

    return render(request, 'accounts/add_certification.html', {'form': form})

from django.contrib.auth import login
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:dashboard')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})