from .models import Flavor, Ingredient, Topping, Packaging
from django.db.models import F

def stock_alerts(request):
    # ---- FLAVORS ----
    critical_flavors = Flavor.objects.filter(quantity__lte=F('critical_threshold'), quantity__gt=0)
    low_flavors = Flavor.objects.filter(quantity__lte=F('low_threshold'), quantity__gt=F('critical_threshold'))

    # ---- INGREDIENTS ----
    critical_ingredients = Ingredient.objects.filter(quantity__lte=2, quantity__gt=0)
    low_ingredients = Ingredient.objects.filter(quantity__lte=5, quantity__gt=2)

    # ---- TOPPINGS ----
    critical_toppings = Topping.objects.filter(quantity__lte=2, quantity__gt=0)
    low_toppings = Topping.objects.filter(quantity__lte=5, quantity__gt=2)

    # ---- PACKAGING ----
    critical_packaging = Packaging.objects.filter(quantity__lte=2, quantity__gt=0)
    low_packaging = Packaging.objects.filter(quantity__lte=5, quantity__gt=2)

    # Total alert count
    total_count = (
        critical_flavors.count() + low_flavors.count() +
        critical_ingredients.count() + low_ingredients.count() +
        critical_toppings.count() + low_toppings.count() +
        critical_packaging.count() + low_packaging.count()
    )

    return {
        "critical_flavors": critical_flavors,
        "low_flavors": low_flavors,

        "critical_ingredients": critical_ingredients,
        "low_ingredients": low_ingredients,

        "critical_toppings": critical_toppings,
        "low_toppings": low_toppings,

        "critical_packaging": critical_packaging,
        "low_packaging": low_packaging,

        "notification_count": total_count,
    }
