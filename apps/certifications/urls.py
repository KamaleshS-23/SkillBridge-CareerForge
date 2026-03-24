from django.urls import path
from . import views

app_name = 'certifications'

urlpatterns = [
    path('dashboard/', views.certification_dashboard, name='certification_dashboard'),
    path('sync/', views.sync_certifications, name='sync_certifications'),
    path('sync/<str:provider>/', views.sync_certifications, name='sync_provider'),
    path('stats/', views.certification_stats, name='certification_stats'),
    path('list/', views.certification_list, name='certification_list'),
    path('clear-cache/', views.clear_cache, name='clear_cache'),
]
