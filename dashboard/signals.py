from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Flavor, Ingredient, Topping, Packaging
from sidebar.models import Inventory

def update_inventory(instance, category):
    item, created = Inventory.objects.get_or_create(
        product_name=instance.name,
        category=category,
        defaults={
            'stock': getattr(instance, 'stock', getattr(instance, 'quantity', 0)),
            'status': 'In Stock',
        }
    )

    # Update stock and status
    item.stock = getattr(instance, 'stock', getattr(instance, 'quantity', 0))
    if item.stock == 0:
        item.status = 'Out of Stock'
    elif item.stock <= 5:
        item.status = 'Low Stock'
    else:
        item.status = 'In Stock'
    item.save()

@receiver(post_save, sender=Flavor)
def sync_flavor_to_inventory(sender, instance, **kwargs):
    update_inventory(instance, 'FLAVORS')

@receiver(post_save, sender=Ingredient)
def sync_ingredient_to_inventory(sender, instance, **kwargs):
    update_inventory(instance, 'INGREDIENTS')

@receiver(post_save, sender=Topping)
def sync_topping_to_inventory(sender, instance, **kwargs):
    update_inventory(instance, 'TOPPINGS')

@receiver(post_save, sender=Packaging)
def sync_packaging_to_inventory(sender, instance, **kwargs):
    update_inventory(instance, 'PACKAGING')

@receiver(post_delete, sender=Flavor)
@receiver(post_delete, sender=Ingredient)
@receiver(post_delete, sender=Topping)
@receiver(post_delete, sender=Packaging)
def delete_from_inventory(sender, instance, **kwargs):
    Inventory.objects.filter(product_name=instance.name).delete()
