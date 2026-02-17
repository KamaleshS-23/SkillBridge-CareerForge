from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('skills/', include('apps.skills.urls')),
    path('jobs/', include('apps.jobs.urls')),
    path('learning/', include('apps.learning.urls')),
    path('assessments/', include('apps.assessments.urls')),
    path('interviews/', include('apps.interviews.urls')),
    path('resumes/', include('apps.resumes.urls')),
    path('certifications/', include('apps.certifications.urls')),
    path('progress/', include('apps.progress.urls')),
    path('api/', include('apps.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)