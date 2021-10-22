from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
# Allows db queries to be ORed when the default is AND
from .models import Image

# Code template from the Boutique Ado mini project tutorial


def all_images(request):

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
    Collects images ids for display in the carousel
    """

    images = request.session.get('images', {})
    images[image_id] = image_id
    request.session['images'] = images

    redirect_url = request.POST.get('redirect_url')

    return redirect(redirect_url)


def carousel_run(request):
    """
    Find the selected images and runs the image carousel
    """

    images_dict = request.session['images']
    images_list = dict.values(images_dict)
    images_select = Image.objects.filter(pk__in=images_list)
    download_paidfor = True

    context = {
        'images': images_select,
        'download_paidfor': download_paidfor,
    }

    return render(request, 'images/carousel.html', context)
