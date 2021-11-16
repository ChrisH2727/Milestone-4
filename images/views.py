from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
# Allows db queries to be ORed when the default is AND
from .models import Image
# from profiles.models import UserImages

# Code template from the Boutique Ado mini project tutorial


def all_images(request):
    """
    Displays images and icons
    """
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
    
    if request.session.get('images', None):
        image_select = int(request.session.get('images', None))
        del request.session['images']

    else:
        image_select = None

    context = {
        'images': images,
        'search_item': query,
        'image_select': image_select,
    }

    return render(request, 'images/images.html', context)


def image_buy(request, image_id):
    """
    Responds to the shopping trolly icon
    and adds immage to the session variable
    """
    # Confirm that the user has credits available
    # credits_available = get_object_or_404(UserCredits, username=request.user)
    print(request.user)
    # check if image previusly downloaded by user
    image = get_object_or_404(Image, pk= image_id)

    print("*********************************",image.image)
    print("++++++++++++++++++++++++++++++++++++", request.user)

    #if not UserImages.objects.filter(images_purchased=image.image).exists():
        # save downloaded image her
        # image_instance = UserImages(username=request.user, images_purchased=image.image)
        #image_instance.save()

        #if credits_available.credits > 0:
        #    credits_available.credits -= 1
        #    credits_available.save()
        #    messages.success(request, f'You have: {credits_available.credits}\
        #        credits remaining')

        #    request.session['images'] = image_id
        #else:
        #    messages.error(
        #        request, f'You have: {credits_available.credits}\
        #            credits remaining')
        #    request.session['images'] = None
    #else:
    #    messages.success(request, 'You already have this image ')

    return redirect(all_images)


def image_info(request, image_ident):
    """
    Displays image details
    """

    del request.session['images']
    image_details = get_object_or_404(Image, pk=int(image_ident))
    messages.error(
        request, f'Image: {image_details.name}',
        f'file size: {image_details.size}')

    return redirect(all_images)
