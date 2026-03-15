from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Certification, CertificationCatalog


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        'username',
        'email',
        'user_type',
        'field_of_interest',
        'is_staff',
        'is_active',
    )

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": (
                "user_type",
                "field_of_interest",
                "profile_picture",
                "phone_number",
                "location",
                "linkedin_url",
                "github_url",
                "portfolio_url",
                "bio",
                "date_of_birth",
            )
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Certification)
admin.site.register(CertificationCatalog)