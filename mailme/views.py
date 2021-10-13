from django.shortcuts import render
from images.models import Category

# Create your views here.


def image_request(request):

    categories = Category.objects.all()
    print (type(categories))
    context = {
        'categories': categories,
    }

    return render(request, 'mailme/mailme.html', context)
