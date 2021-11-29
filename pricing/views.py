from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Subscription, Order, Trolly
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
    # Delete trolly contents
    Trolly.objects.all().delete()
    
    subscriptions = Subscription.objects.all()
    subscription_id =1
    button_state = "add"        
    template = 'pricing/pricing.html'

    context = {
            'subscriptions': subscriptions,
            'button_state': button_state,
            'toggle_id': int(subscription_id),
        }
    return render(request, template, context)

@login_required
def trolly_add(request, subscription_id):
    """
    Adds the selected subscription option to the trolly
    calls for the payment form to be generated
    """
    
    # Delete trolly contents
    Trolly.objects.all().delete()
    button_state = "add"
    
    subscription_details = get_object_or_404(Subscription, pk=subscription_id)

    # Toggle subscription in the trolly
    if Trolly.objects.filter(sku= subscription_details.sku).exists():
        Trolly.objects.filter(sku= subscription_details.sku).delete()
        
    else:
        Trolly.objects.update_or_create(
            sku= subscription_details.sku,
            price= subscription_details.sub_price,
            sub_display_name= subscription_details.sub_display_name,
            credits= subscription_details.sub_images,
            sub_count =1
            )
        button_state = "added"

    subscriptions = Subscription.objects.all()

    template = 'pricing/pricing.html'
    context = {
            'subscriptions': subscriptions,
            'button_state': button_state,
            'toggle_id': int(subscription_id),
        }
    return render(request, template, context)


@login_required
def trolly_delete(request, subscription_id):
    """
    Handles removal of item from the trolly
    """
    
    Trolly.objects.get(pk=subscription_id).delete()

    messages.success(request, 'Subscripion deteleted from the trolly.')

    return redirect(showtrolly)


@login_required
def showtrolly(request):
    """
    Handles order summary
    """
    trolly_items = Trolly.objects.all()
    if trolly_items:
        subscriptions_total = Trolly.objects.all().aggregate(Sum('price'))
        for key, value in subscriptions_total.items():
            net_total = float(value)

        context = {
            'net_total': net_total,
            'sales_tax': settings.SALES_TAX_RATE/100 * net_total,
            'grand_total': (settings.SALES_TAX_RATE/100 * net_total) + net_total,
            'sales_tax_rate':settings.SALES_TAX_RATE,
            'trolly_items': trolly_items,
            }
        return render(request, 'pricing/showtrolly.html', context)
    else:
        messages.success(request, 'Your trolly is empty!')
    
    return redirect(pricing)


def payment_request(request):
    """
    Handles order payment request
    """

    # Built from Stripe code & Code Institute Boutique Ado tutorial
    # Initially stripped out to just the bare bones and then re-
    # built to provide the required functionality for this application

    # checkout only if the trolly has content
    trolly_items = Trolly.objects.all()
    if trolly_items:
        subscriptions_total = Trolly.objects.all().aggregate(Sum('price'))
        for key, value in subscriptions_total.items():
            net_total = float(value)
            stripe_total = int(value)*100

        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY

        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                open_form = form.save(commit=False)
                open_form.order_total = net_total
                open_form.sales_tax_rate = settings.SALES_TAX_RATE
                open_form.sales_tax = settings.SALES_TAX_RATE/100 * net_total
                open_form.grand_total = (settings.SALES_TAX_RATE/100 * net_total) + net_total
                open_form.save()

                messages.success(request, 'Order sucessfully placed added product!')

                # Sum all credits and allocate to the user signed in
                credits_total = Trolly.objects.all().aggregate(Sum('credits'))
                for values in credits_total.values():
                    additional_credits = values

                user = UserProfile.objects.get(user=request.user)
                existing_credits =  user.credits

                existing_credits = existing_credits + additional_credits
                user.credits = existing_credits
                user.save()

                # Delete trolly contents
                Trolly.objects.all().delete()

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



