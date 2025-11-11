from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Flavor(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    expiration_date = models.DateField(null=True, blank=True)  # 👈 Add this
    created_at = models.DateTimeField(default=timezone.now)    # 👈 Keep if you want timestamps

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()
    expiration_date = models.DateField()

    def __str__(self):
        return self.name

class Topping(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name# ← this field is new


    def __str__(self):
        return self.name


class Packaging(models.Model):
    type = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} ({self.quantity} pcs)"

class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} {self.action} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
