from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User


class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:dashboard')
        return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('core:home')


class RegisterView(View):
    def get(self, request):
        return render(request, 'accounts/register.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        
        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/register.html', {'error': 'Email already exists'})
        
        user = User.objects.create_user(
            email=email,
            username=email,
            password=password,
            user_type=user_type
        )
        login(request, user)
        return redirect('core:dashboard')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    login_url = 'accounts:login'
