from django.shortcuts import render


def pricing_options(request):

    return render(request, 'pricing/pricing.html')
