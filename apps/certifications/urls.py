from django.urls import path
from . import views

app_name = 'certifications'

urlpatterns = [
    path('dashboard/', views.certification_dashboard, name='certification_dashboard'),
    path('sync/', views.sync_certifications, name='sync_certifications'),
    path('stats/', views.certification_stats, name='certification_stats'),
    path('clear-cache/', views.clear_cache, name='clear_cache'),
]
