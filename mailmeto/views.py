from django.shortcuts import render, redirect, get_object_or_404
from images.models import Category
from .forms import RequestForm
from .models import RequestImage
from django.views.decorators.http import require_POST
from django.contrib import messages
from pprint import pprint

def image_request(request):
    """
    Populates image request template
    """
    request_form = RequestForm()
    if request.method == 'POST':
        form = RequestForm(request.POST or None)
        if form.is_valid():
            request_name = form.cleaned_data['request_name']
            image = RequestImage(request_name=request_name)
            image.save()
            return render(request, 'mailmeto/mailme_success.html')
    else:
        context = {
            'request_form': request_form,
        }

    return render(request, 'mailmeto/mailme.html', context)

