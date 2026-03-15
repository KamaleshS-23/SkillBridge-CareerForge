from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Certification


# ✅ Custom User Register Form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'field_of_interest', 'password1', 'password2')


# ✅ Certification Form
class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = [
            'name',
            'organization',
            'issue_date',
            'expiry_date',
            'credential_id',
            'credential_url',
        ]