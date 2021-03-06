from django.contrib import admin
from .models import Subscription, Trolly, Order

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'full_name',
        'company_name',
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
        'sub_display_price',
    )


class TrollyAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'price',
        'sub_count',
    )

# Register Subscription model.
admin.site.register(Subscription, SubscriptionAdmin)

# Register Order model.
admin.site.register(Order, OrderAdmin)

# Register Trolly model.
admin.site.register(Trolly, TrollyAdmin)
