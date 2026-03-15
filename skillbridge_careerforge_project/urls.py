from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Core App
    path('', include('apps.core.urls')),

    # Accounts App
    path('accounts/', include('apps.accounts.urls')),

    # Feature Apps
    path('skills/', include('apps.skills.urls')),
    path('jobs/', include('apps.jobs.urls')),
    path('learning/', include('apps.learning.urls')),
    path('assessments/', include('apps.assessments.urls')),
    path('interviews/', include('apps.interviews.urls')),
    path('resumes/', include('apps.resumes.urls')),
    path('certifications/', include('apps.certifications.urls')),
    path('progress/', include('apps.progress.urls')),

    # API
    path('api/', include('apps.api.urls')),
]

# Static & Media (Development Only)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)