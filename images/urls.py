from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_images, name='images'),
    path('<image_id>', views.carousel, name='carousel'),
]
