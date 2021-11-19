from django.contrib import admin
from .models import UserProfile, UserImages


class UserProfileAdmin(admin.ModelAdmin):
    """
    Test and manage user accounts
    """
    list_display = (
        'user',
        'mobile_phone_number',
        'credits',
    )



class UserImagesAdmin(admin.ModelAdmin):
    """
    Test and manage images downloaded by the user
    """
    list_display = (
        'username',
        'images_purchased',
    )


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserImages, UserImagesAdmin)
