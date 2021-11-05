from django.urls import path
from . import views

urlpatterns = [
    path('', views.management, name='management'),
    path('edit_request/<int:request_id>', views.edit_request, name='edit_request'),
    path('delete_request/<int:request_id>', views.delete_request, name='delete_request'),
    path('edit_request/', views.edit_request, name='edit_request'),
    path('', views.edit_request, name='edit_request'),  
]