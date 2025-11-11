from django.contrib import admin
from .models import LogHistory, Inventory

admin.site.register(LogHistory)

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'stock', 'status', 'last_updated')
    search_fields = ('product_name', 'category')
    list_filter = ('status', 'category')