from django.contrib import admin
from .models import Subscription


class Subscription(admin.SubscriptionAdmin):
    list_display = (
        'sub_type',
        'sub_name',
        'sub_display_name',
        'sub_display_description',
        'sub_duration',
        'sub_images',
        'sub_price',
    )

# Register Subscription models.

admin.site.register(Subscription, SubscriptionAdmin)