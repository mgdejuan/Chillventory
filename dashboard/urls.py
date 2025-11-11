from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Flavors CRUD
    path('flavors/', views.flavors, name='flavors'),
    path('flavors/delete/<int:delete_id>/', views.delete_flavor, name='delete_flavor'),

    # Ingredients CRUD
    path('ingredients/', views.ingredients, name='ingredients'),
    path('ingredients/delete/<int:delete_id>/', views.delete_ingredient, name='delete_ingredient'),

    # Toppings CRUD
    path('toppings/', views.toppings, name='toppings'),
    path('toppings/delete/<int:id>/', views.delete_topping, name='delete_topping'),

    # Packaging CRUD
    path('packaging/', views.add_packaging, name='packaging'),
    path('packaging/delete/<int:id>', views.delete_packaging, name='delete_packaging'),
    path('add_packaging/', views.add_packaging, name='add_packaging'),
    # Logs
    path('log-history/', views.log_history, name='log_history'),

    path('', views.dashboard, name='dashboard'),
    path('log-history/', views.log_history, name='log_history'),
]
