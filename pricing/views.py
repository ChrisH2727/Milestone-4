from django.shortcuts import render
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

import stripe
import json

def pricing(request):

    return render(request, 'pricing/pricing.html')


def pricing_options(request):
# From Code Institute Boutique Ado tutorial

    # Set a temporary total to get stripe working
    total = 0.99
    stripe_total = round(total*100)
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    stripe.api_key = stripe_secret_key

    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    context = {
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'stripe_total': stripe_total,
    }

    return render(request, 'pricing/checkout.html', context)

