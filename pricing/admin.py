from django.contrib import admin
from .models import Subscription, Trolly, Order

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'full_name',
        'email',
        'mobile_phone_number',
        'date',
        'order_total',
        'sales_tax_rate',
        'sales_tax',
        'grand_total',
        'stripe_pid',
        'completed',
    )

 
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

# Register Order model.
admin.site.register(Order, OrderAdmin)
