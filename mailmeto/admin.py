from django.contrib import admin
from .models import RequestImage


class RequestAdmin(admin.ModelAdmin):
    list_display = (
        'category',
        'request_name',
        'request_email',
        'description',
        'image'
        )


# Register Request_image db.
admin.site.register(RequestImage, RequestAdmin)
