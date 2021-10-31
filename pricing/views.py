from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .models import Subscription
from django.db.models import Sum

import stripe
import json


def pricing(request):
    """
    Renders the subscription template and
    passes the subscription object through.
    """

    subscriptions = Subscription.objects.all()

    template = 'pricing/pricing.html'

    context = {
            'subscriptions': subscriptions
        }
    return render(request, template, context)


def trolly_add(request, subscription_id):
    """
    Adds the selected subscription option to the trolly
    calls for the payment form to be generated
    """
    subscription_details = get_object_or_404(Subscription, pk=subscription_id)

    trolly_content = request.session.get('trolly', {})

    trolly_content[subscription_id] = subscription_details.sku
    request.session['trolly'] = trolly_content

    return redirect(pricing)


def payment_request(request):

    # Built from Stripe code & Code Institute Boutique Ado tutorial
    # Initially stripped out to just the bare bones and then re-
    # built to provide the required functionality for this application
    print("payment_request")

    trolly_dict = request.session['trolly']
    trolly_values = dict.values(trolly_dict)
    # subscriptions to display in the order summary
    subscriptions_select = Subscription.objects.filter(sku__in=trolly_values)

    # subscriptions to calculate total cost
    subscriptions_total = Subscription.objects.filter(
        sku__in=trolly_values).aggregate(Sum('sub_price'))

    for key, value in subscriptions_total.items():
        stripe_total = int(value)

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        form_data = {
            'full_name': request.POST['full_name'],
        }
        print("posted")
        return redirect(reverse('checkout_success'))

    else:
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
            'subscriptions': subscriptions_select,
        }

    return render(request, 'pricing/checkout.html', context)

def checkout_success(request):
    """
    Handles a sucessful checkout
    """
    messages.success(request, f'Order processed')
        
    template = "pricing/checkout_success.html"

    return render(request, template)

