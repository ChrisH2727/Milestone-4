from django.http import HttpResponse
from .email_handler import send_order_confirmation_email
from .models import Order

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
        intent = event.data.object
        
        # Find orders that have been placed but no response email sent
        payments_made = Order.objects.filter(completed=False)
        
        for key, value in payments_made.items():
            print("payments", payments_made)

        
        
        #for payments in payments_made:
        #    print("payments_made", payments_made[id])

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        intent = event.data.object
        
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
