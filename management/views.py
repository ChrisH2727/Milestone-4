from django.shortcuts import render, get_object_or_404, redirect
from mailmeto.models import RequestImage
from .forms import ResponseForm

def management(request):
    """
    Populates image response template
    """

    requests = RequestImage.objects.all()

    context = {
        'requests': requests,
    }

    return render(request, 'management/management.html', context)

#@login_required
def edit_request(request, request_id):
    """
    Edit the request for an image
    """

    request_for_image = get_object_or_404(RequestImage, id=request_id)
    form = ResponseForm(instance=request_for_image)

    response_form = ResponseForm()
    if request.method == 'POST':
        form = RequestForm(request.POST or None)

        # save image request 
        if form.is_valid():
            request_name = form.cleaned_data['request_name']
            request_email = form.cleaned_data['request_email']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            image = RequestImage(
                request_name=request_name,
                request_email=request_email,
                description=description,
                category=category
                )
            image.save()

            # display confirmation message 
            #messages.success(request, f'Image request successfully processed! \
            #A confirmation email will be sent to {request_email}.')

            # send confirmation email
            #image_response = {
            #    'request_name': request_name,
            #    'request_email': request_email,
            #    'description': description,
            #    'category': category
            #}
            #send_confirmation_email(image_response)

            return redirect(management)
    else:
        template = 'management/edit_request.html'
        context = {
            'form': form,
        }

    return render(request, template, context)
    


#@login_required
def delete_request(request, request_id):
    """
    Delete the request for an image
    """
    request_for_image = get_object_or_404(RequestImage, id=request_id)
    form = ResponseForm(instance=request_for_image)

    template = 'management/delete_request.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
