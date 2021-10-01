from django.contrib import admin
from .models import Image, Category


class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'sku',
        'views',
        'downloads',
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'display_name',
        'name',
    )

# Register Image and Category models.


admin.site.register(Image, ImageAdmin)
admin.site.register(Category, CategoryAdmin)
