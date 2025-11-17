from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Flavors CRUD
    path('flavors/', views.flavors, name='flavors'),
    path('flavors/delete/<int:id>/', views.delete_flavor, name='delete_flavor'),

    # Ingredients CRUD
    path('ingredients/', views.ingredients, name='ingredients'),
    path('ingredients/delete/<int:id>/', views.delete_ingredient, name='delete_ingredient'),

    # Toppings CRUD
    path('toppings/', views.toppings, name='toppings'),
    path('toppings/delete/<int:id>/', views.delete_topping, name='delete_topping'),

    # Packaging CRUD
    path('packaging/', views.add_packaging, name='packaging'),
    path('packaging/delete/<int:id>', views.delete_packaging, name='delete_packaging'),
    path('add_packaging/', views.add_packaging, name='add_packaging'),
    # Logs
    path('log-history/', views.log_history, name='log_history'),
    
    # Inventory dashboard
    path('inventory/', views.inventory, name='inventory'),
    
    path('inventory/restock/flavor/<int:id>/', views.restock_flavor, name='restock_flavor'),
    path('inventory/restock/ingredient/<int:id>/', views.restock_ingredient, name='restock_ingredient'),
    path('inventory/restock/topping/<int:id>/', views.restock_topping, name='restock_topping'),
    path('inventory/restock/packaging/<int:id>/', views.restock_packaging, name='restock_packaging'),

    # Log history
    path('logs/', views.log_history, name='log_history'),
]
