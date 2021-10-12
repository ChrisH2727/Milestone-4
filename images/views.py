from django.shortcuts import render
from .models import Image

# Create your views here.


def all_images(request):

    images = Image.objects.all()


    context = {
         'images': images,
    }
    for image in images:
         print(image)

    return render(request, 'images/images.html', context)

