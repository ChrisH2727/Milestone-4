from django.contrib import admin
from .models import RequestImage


class RequestAdmin(admin.ModelAdmin):
    list_display = (
        'request_number',
        'request_date',
        'category',
        'request_name',
        'request_email',
        'description',
        'image',
        'availability_date'
        )


# Register Request_image db.
admin.site.register(RequestImage, RequestAdmin)
