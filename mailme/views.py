from django.shortcuts import render
from images.models import Category
from .forms import RequestForm


def image_request(request):

    request_form = RequestForm()

    context = {
        'request_form': request_form,
    }

    return render(request, 'mailme/mailme.html', context)

def process_request(request):
    """
    Processes a requests for an image and emails the user
    """

    return render(request, 'mailme/mailme_success.html')
