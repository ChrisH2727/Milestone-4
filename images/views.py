from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
# Allows db queries to be ORed when the default is AND
from .models import Image

# Code template from the Boutique Ado mini project tutorial

def all_images(request):
    print("all images")

    images = Image.objects.all()
    query = None

    if request.GET:
        if "q" in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "No image requested.")
                return redirect(reverse("images"))

            queries = Q(name__icontains=query) | Q(
                dimensions__icontains=query)
            # Pipe provides OR i makes search case insensitive
            images = images.filter(queries)

    context = {
        'images': images,
        'search_item': query
    }

    return render(request, 'images/images.html', context)


def carousel(request, image_id):
    """
    Expand the image to take up the whole screen and
    allow the user further images in a carousel
    """

    image = get_object_or_404(Image, pk=image_id)
    redirect_url = request.POST.get('redirect_url')
    print(image_id)
    
    return redirect(redirect_url)
