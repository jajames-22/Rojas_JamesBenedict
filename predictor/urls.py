from django.urls import path
from . import views

urlpatterns = [
    path('', views.predict_quality, name='predict'),
    path('data/', views.view_data, name='view_data'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('delete/<int:pk>/', views.delete_record, name='delete_record'),
    
    # NEW URLs for Add and Edit
    path('add/', views.add_record, name='add_record'),
    path('edit/<int:pk>/', views.edit_record, name='edit_record'),
]