from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.image_management, name='image_management'),
    path('image_management_edit/<int:ask_id>/', views.image_management_edit, name='image_management_edit'),
    path('image_management_delete/<int:ask_id>/', views.image_management_delete, name='image_management_delete'),
    path('image_management_delete/', views.image_management_delete, name='image_management_delete'),
    path('<int:ask_id>/', views.image_management_add, name='image_management_add'),
    path('', views.image_management_add, name='image_management_add'),
    path('image_management/', views.image_management, name='image_management'),
    path('add_image/', views.image_management_add, name='image_management_add'),
]
