from django.contrib import admin
from .models import Subscription, Trolly


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'sub_type',
        'sub_name',
        'sub_display_name',
        'sub_display_description',
        'sub_duration',
        'sub_images',
        'sub_price',
    )


class TrollyAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'dispaly_name',
        'sub_display_name',
        'sub_price',
        'image',
    )

# Register Subscription model.
admin.site.register(Subscription, SubscriptionAdmin)
