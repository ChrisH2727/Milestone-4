from django.http import HttpResponse
from .email_handler import send_order_confirmation_email
from .models import Order
#from django.contrib import messages

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """

        # messages.error(request, 'payment intent received')

        intent = event.data.object
        
        # Find orders that have been placed but no response email sent
        # and send confirmation email
        for order in Order.objects.all():
            if not order.completed:
                order_details = {
                    'full_name': order.full_name,
                    'email': order.email,
                    'order_number': order.order_number,
                    'company_name': order.company_name,
                    'address_line_1': order.address_line_1,
                    'address_line_2': order.address_line_2,
                    'town_or_city': order.town_or_city,
                    'county': order.county,
                    'date': order.date,
                    'order_total': order.order_total,
                    'sales_tax_rate': order.sales_tax_rate,
                    'sales_tax': order.sales_tax,
                    'grand_total': order.grand_total
                    }
                send_order_confirmation_email(order_details)
                order.completed = True
                order.save()

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        intent = event.data.object
        #messages.error(request, 'payment intent failed')
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
