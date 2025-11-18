from django.db import models
from django.contrib.auth.models import User
from django.db.models import F

# ----------------- FLAVOR -----------------
class Flavor(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    expiration_date = models.DateField(null=True, blank=True)
    low_threshold = models.IntegerField(default=5)
    critical_threshold = models.IntegerField(default=2)

    def __str__(self):
        return self.name

# ----------------- INGREDIENT -----------------
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

# ----------------- TOPPING -----------------
class Topping(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

# ----------------- PACKAGING -----------------
class Packaging(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.name

# ----------------- LOG -----------------
class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action[:30]}"

# ----------------- STOCK ALERTS -----------------
def stock_alerts(request):
    """
    Returns stock alerts for flavors, ingredients, and toppings.
    Can be used as a context processor for templates.
    """
    critical_flavors = Flavor.objects.filter(quantity__lte=F('critical_threshold'), quantity__gt=0)
    low_flavors = Flavor.objects.filter(quantity__lte=F('low_threshold'), quantity__gt=F('critical_threshold'))

    critical_ingredients = Ingredient.objects.filter(quantity__lte=2, quantity__gt=0)
    low_ingredients = Ingredient.objects.filter(quantity__lte=5, quantity__gt=2)

    critical_toppings = Topping.objects.filter(quantity__lte=2, quantity__gt=0)
    low_toppings = Topping.objects.filter(quantity__lte=5, quantity__gt=2)

    return {
        'critical_flavors': critical_flavors,
        'low_flavors': low_flavors,
        'critical_ingredients': critical_ingredients,
        'low_ingredients': low_ingredients,
        'critical_toppings': critical_toppings,
        'low_toppings': low_toppings,
    }

class Notification(models.Model):
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.message