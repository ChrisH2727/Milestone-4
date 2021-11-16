from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    """
    Test and manage user accounts
    """
    list_display = (
        'user',
        'mobile_phone_number',
    )


#class UserCreditsAdmin(admin.ModelAdmin):
#    """
#    Test and manage user credits purchased 
#    """
#    list_display = (
#        'credits',
#        )


#class UserImagesAdmin(admin.ModelAdmin):
#    """
#    Test and manage images downloaded by the user
#    """
#    list_display = (
#        'images_purchased',
#    )


admin.site.register(UserProfile, UserProfileAdmin)
# admin.site.register(UserCredits, UserCreditsAdmin)
#admin.site.register(UserImages, UserImagesAdmin)
