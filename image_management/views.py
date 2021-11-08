from images.models import Image
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def image_management(request):
    """
    Populates image inventory management_template
    """
    images = Image.objects.all()

    context = {
        'images': images,
    }

    return render(request, 'image_management/image_management.html', context)


