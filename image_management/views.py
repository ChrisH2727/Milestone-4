from images.models import Image
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageManagementForm


@login_required
def image_management(request):
    """
    Populates image inventory management_template
    """

     # Confirm superuser
    if not request.user.is_superuser:
        messages.error(request, 'Reserver for site operators.')
        return redirect(reverse('home'))

    images = Image.objects.all()

    context = {
        'images': images,
    }

    return render(request, 'image_management/image_management.html', context)


@login_required
def image_management_add(request):
    """
    Populates image inventory management template
    """

    # Confirm superuser
    if not request.user.is_superuser:
        messages.error(request, 'Reserver for site operators.')
        return redirect(reverse('home'))

    add_image_form = ImageManagementForm()
    if request.method == 'POST':
        form = ImageManagementForm(request.POST or None)
        # save image request 
        if form.is_valid():
            # initialise unviewed fields
            open_form = form.save(commit=False)
            open_form.views = 0
            open_form.downloads = 0
            open_form.price = 1.00
            form.save()

            # display confirmation message 
            messages.success(request, 'Image detailes have been generated')

        else:
            # display confirmation message 
            messages.success(request, 'Failed to generate image details')

        return redirect(image_management)
    else:
        context = {
            'add_image_form': add_image_form,
            }

    return render(request, 'image_management/add_image.html', context)

@login_required
def image_management_edit(request, ask_id):
    """
    Edit the request for an image
    """
    # Confirm superuser
    if not request.user.is_superuser:
        messages.error(request, 'Reserver for site operators.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        response_form = ImageManagementForm(request.POST)
        # save image request
        if response_form.is_valid():
            # display confirmation message
            messages.success(request,'Image details updated')

            # Update the request
            Image.objects.filter(id=ask_id).update(
                image=response_form.cleaned_data['image'],
                name=response_form.cleaned_data['name'],
                )
            messages.success(request, 'Image request updated')

            return redirect(image_management)

        else:
            messages.error(request, 'Please complete the form correctly')

    else:
        request_for_image = get_object_or_404(Image, id=ask_id)
        form = ImageManagementForm(instance=request_for_image)
    
    template = 'image_management/image_management_edit.html'

    context = {
        'form': form,
        'ask_id': ask_id,
        }

    return render(request, template, context)


@login_required
def image_management_delete(request, ask_id):
    """
    Delete the request for an image
    """
    # Confirm superuser
    if not request.user.is_superuser:
        messages.error(request, 'Reserver for site operators.')
        return redirect(reverse('home'))

    form = ImageManagementForm()
    if request.method == 'POST':
        response_form = ImageManagementForm(request.POST)

        # delete image request 
        if response_form.is_valid():
            # delete the image request
            Image.objects.filter(id=ask_id).delete()

            messages.success(request, 'Image request deleted')
            return redirect(image_management)
        else:
            messages.error(request, 'The image request has not been deleted.')

    else:
        request_for_image = get_object_or_404(Image, id=ask_id)
        form = ImageManagementForm(instance=request_for_image)

    template = 'image_management/image_management_delete.html'

    context = {
        'form': form,
        'ask_id': ask_id,
        }

    return render(request, template, context)
