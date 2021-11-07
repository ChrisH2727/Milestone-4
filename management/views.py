from django.shortcuts import render, get_object_or_404, redirect
from mailmeto.models import RequestImage
from .forms import ResponseForm
from django.contrib import messages

def management(request):
    """
    Populates image response template
    """
    requests = RequestImage.objects.all()

    context = {
        'requests': requests,
    }

    return render(request, 'management/management.html', context)


def edit_request(request, ask_id):
    """
    Edit the request for an image
    """
    print("edit_request ", ask_id)
    if request.method == 'POST':
        response_form = ResponseForm(request.POST)
        # save image request 
        if response_form.is_valid():
            print("form valid")
            response_form.save()

            # send confirmation email
            #send_confirmation_email(image_response)

            return redirect(management)
        else:
            messages.error(request, f'Please complete the form correctly')
            print("form not valid")

    else:
        request_for_image = get_object_or_404(RequestImage, id=ask_id)
        form = ResponseForm(instance=request_for_image)
    
    template = 'management/edit_request.html'
    context = {
        'form': form,
        }

    return render(request, template, context)
    


def delete_request(request, request_id):
    """
    Delete the request for an image
    """
    request_for_image = get_object_or_404(RequestImage, id=request_id)
    form = ResponseForm(instance=request_for_image)

    # response_form = ResponseForm()
    if request.method == 'POST':
        form = RequestForm(request.POST or None)
        print("post")
        return redirect(management)
    else:
        template = 'management/delete_request.html'
        print("get")
        context = {
            'form': form,
        }

    return render(request, template, context)
