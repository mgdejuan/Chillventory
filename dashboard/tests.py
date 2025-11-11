# dashboard/urls.py

from django.urls import path
from .views import (
    FlavorListView, 
    FlavorDetailView, 
    FlavorCreateView, 
    FlavorUpdateView, 
    FlavorDeleteView
)

urlpatterns = [
    # READ (List All)
    path('', FlavorListView.as_view(), name='flavor_list'), 
    
    # CREATE
    path('new/', FlavorCreateView.as_view(), name='flavor_create'),
    
    # READ (Detail Single)
    path('<int:pk>/', FlavorDetailView.as_view(), name='flavor_detail'),
    
    # UPDATE
    path('<int:pk>/edit/', FlavorUpdateView.as_view(), name='flavor_update'),
    
    # DELETE
    path('<int:pk>/delete/', FlavorDeleteView.as_view(), name='flavor_delete'),
]