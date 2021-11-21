from django.contrib import admin
from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.pricing, name='pricing'),
    path('pricing/<subscription_id>', views.trolly_add, name='trolly_add'),
    path('checkout/<subscription_id>', views.trolly_delete, name='trolly_delete'),
    #path('pricing/', views.payment_request, name='payment_request'),
    path('pricing/', views.showtrolly, name='showtrolly'),
    path('showtrolly/', views.payment_request, name='payment_request'),
    path('pricing/', views.checkout_success, name='checkout_success'),
    path('wh/', webhook, name='webhook'),
]
