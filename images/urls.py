from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_images, name='images'),
    path('images/<image_id>', views.image_buy, name='image_buy'),
]
