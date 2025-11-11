from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Flavors
    path('flavors/', views.flavors, name='flavors'),  # add / list
    path('flavors/delete/<int:delete_id>/', views.delete_flavor, name='delete_flavor'),  # delete inline

    path('ingredients/', views.ingredients, name='ingredients'),
    path('ingredients/delete/<int:ingredient_id>/', views.delete_ingredient, name='delete_ingredient'),

    path('toppings/', views.toppings, name='toppings'),
    path('toppings/update/<int:topping_id>/', views.toppings, name='update_topping'),
    path('toppings/delete/<int:id>/', views.delete_topping, name='delete_topping'),


    path('packaging/', views.packaging, name='packaging'),
    path('packaging/update/<int:packaging_id>/', views.packaging, name='update_packaging'),
    path('packaging/delete/<int:id>/', views.delete_packaging, name='delete_packaging'),

    path('log-history/', views.log_history, name='log_history'),
]
