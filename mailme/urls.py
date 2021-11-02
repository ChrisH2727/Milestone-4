from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.image_request, name='mailme'),
    path('mailme/', views.process_request, name='process_request'),
]