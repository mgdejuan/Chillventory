from django.db import models
from django.contrib.auth.models import User

# ----------------- FLAVOR -----------------
class Flavor(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    expiration_date = models.DateField(null=True, blank=True)

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

    def __str__(self):
        return self.name


# ----------------- LOG -----------------
class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action[:30]}"

