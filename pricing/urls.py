from django.contrib import admin
from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.pricing, name='pricing'),
    path('pricing/', views.pricing_options, name='pricing_options'),
    # path('pricing/', views.checkout, name='checkout'),
    path('wh/', webhook, name='webhook'),
]
