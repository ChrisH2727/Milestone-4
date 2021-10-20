from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from images.models import Image


def carousel_contents(request):

    carousel_items = []
    carousel_count = 0

    context = {
        'carousel_items': carousel_items,
        'carousel_count': carousel_count,
    }

    return context