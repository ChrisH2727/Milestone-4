from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_images, name='images'),
    path('<image_id>', views.carousel, name='carousel'),
    path('images/', views.carousel_run, name='carousel_run'),
    path('images/', views.image_download, name='image_download'),
]
