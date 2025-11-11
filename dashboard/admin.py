from django.contrib import admin
from .models import Flavor, Ingredient, Topping, Packaging

@admin.register(Flavor)
class FlavorAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_available', 'created_at')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'is_available', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_available', 'created_at')


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_available', 'created_at')


@admin.register(Packaging)
class PackagingAdmin(admin.ModelAdmin):
    list_display = ('type', 'cost', 'is_available', 'created_at')
    search_fields = ('type',)
    list_filter = ('is_available', 'created_at')
