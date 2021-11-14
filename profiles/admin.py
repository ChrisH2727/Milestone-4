from django.contrib import admin
from .models import UserProfile, UserCredits


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'mobile_phone_number',
    )


class UserCreditsAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'credits',
        )

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserCredits, UserCreditsAdmin)