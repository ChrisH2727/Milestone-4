from django.contrib import admin
from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.pricing, name='pricing'),
    path('pricing/', views.pricing_options, name='pricing_options'),
    path('wh/', webhook, name='webhook'),
    path('pricing/', views.checkout_success, name='checkout_success'),
]
