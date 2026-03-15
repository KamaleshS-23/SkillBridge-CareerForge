from django.urls import path
from .views import HomeView, dashboard

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', dashboard, name='dashboard'),
]