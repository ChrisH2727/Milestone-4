from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Subscription, Order
from django.db.models import Sum
from .forms import OrderForm
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from django.conf import settings
from django.contrib.auth.models import User

import stripe
import json

@login_required
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

@login_required
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

@login_required
def trolly_delete(request, subscription_id):
    """
    Handles removal of item from the trolly
    """
    
    trolly_content = request.session.get('trolly', {})

    if subscription_id in trolly_content:
        del trolly_content[subscription_id]
        request.session["trolly_content"] = trolly_content

    messages.success(request, 'Subscripion deteleted from the trolly.')

    return redirect(showtrolly)


@login_required
def showtrolly(request):
    """
    Handles order summary
    """
    # show order summary only if the trolly has content
    if request.session.get('trolly',None):
        messages.success(request, 'show trolly content')
        
        trolly_dict = request.session['trolly']
        trolly_values = dict.values(trolly_dict)
        
        # subscriptions to display in the order summary
        subscriptions_select = Subscription.objects.filter(sku__in=trolly_values)

        # subscriptions to calculate total cost
        subscriptions_total = Subscription.objects.filter(
            sku__in=trolly_values).aggregate(Sum('sub_price'))

        for key, value in subscriptions_total.items():
            stripe_total = int(value)*100
            net_total = float(value)
    
        context = {
            'net_total': net_total,
            'sales_tax': settings.SALES_TAX_RATE/100 * net_total,
            'grand_total': (settings.SALES_TAX_RATE/100 * net_total) + net_total,
            'sales_tax_rate':settings.SALES_TAX_RATE,
            'subscriptions': subscriptions_select,
            }
        return render(request, 'pricing/showtrolly.html', context)
    else:
        messages.success(request, 'trolly is empty')
    
    return redirect(pricing)


def payment_request(request):
    """
    Handles order payment request
    """

    # Built from Stripe code & Code Institute Boutique Ado tutorial
    # Initially stripped out to just the bare bones and then re-
    # built to provide the required functionality for this application

    # checkout only if the trolly has content
    if request.session.get('trolly',None):
        messages.success(request, 'Processing payment request')
        
        trolly_dict = request.session['trolly']
        trolly_values = dict.values(trolly_dict)
        
        # subscriptions to display in the order summary
        subscriptions_select = Subscription.objects.filter(sku__in=trolly_values)

        # subscriptions to calculate total cost
        subscriptions_total = Subscription.objects.filter(
            sku__in=trolly_values).aggregate(Sum('sub_price'))

        for key, value in subscriptions_total.items():
            stripe_total = int(value)*100
            net_total = float(value)

        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY

        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save()
                
                messages.success(request, 'Order sucessfully placed added product!')

                if 'trolly' in request.session:
                    del request.session['trolly']

                user_credits= get_object_or_404(UserProfile, user=request.user)
                credits = get_object_or_404(Subscription, sku__in=trolly_values)
                user_credits.credits = user_credits.credits + credits.sub_images
                user_credits.save()

                return render(request, 'pricing/checkout_success.html')

            else:
                messages.error(request, 'Failed to to place order')

        else:

            profile = UserProfile.objects.get(user=request.user)
            stripe.api_key = stripe_secret_key

            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )

            # Attempt to prefill the form with any info the user 
            # maintains in their profile
            order_form = OrderForm(initial={
                'company_name': profile.company_name,
                'address_line_1':  profile.address_line_1,
                'address_line_2':  profile.address_line_2,
                'town_or_city':  profile.town_or_city,
                'county':  profile.county,
                'postcode':  profile.postcode,
                'country':  profile.country,
                'email': profile.user.email,
                'order_total': net_total,
                'grand_total': (
                    settings.SALES_TAX_RATE/100 * net_total) + net_total,
                })
            
            if not stripe_public_key:
                messages.warning(request, 'Stripe public key is missing. \
                Did you forget to set it in your environment?')

            context = {
                'net_total': net_total,
                'grand_total': (settings.SALES_TAX_RATE/100 * net_total) + net_total,
                'order_form': order_form,
                'stripe_public_key': stripe_public_key,
                'client_secret': intent.client_secret,
                }

        return render(request, 'pricing/checkout.html', context)
    
    else:
        messages.error(request, 'No subscription options selected.')
    
    return redirect(pricing)


def checkout_success(request):
    """
    Handles a sucessful checkout and clears out the trolly
    """
   
    messages.success(request, 'Order processed')
        
    template = "pricing/checkout_success.html"

    return render(request, template)



