from django.contrib import admin
from .models import Flavor, Ingredient, Topping, Packaging

@admin.register(Flavor)
class FlavorAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'expiration_date')
    search_fields = ('name',)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'expiration_date')
    search_fields = ('name',)


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'expiration_date')
    search_fields = ('name',)


@admin.register(Packaging)
class PackagingAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity')
    search_fields = ('name',)
