from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class LogHistory(models.Model):
    ACTION_CHOICES = [
        ('LOGIN', 'Login'),
        ('ADD', 'Add'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]

    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action_taken = models.CharField(max_length=20, choices=ACTION_CHOICES)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    stock_status = models.CharField(max_length=50, blank=True, null=True)
    date_and_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.staff} - {self.action_taken} - {self.date_and_time.strftime('%Y-%m-%d %H:%M')}"

from django.db import models

class Inventory(models.Model):
    CATEGORY_CHOICES = [
        ('FLAVORS', 'Flavors'),
        ('INGREDIENTS', 'Ingredients'),
        ('TOPPINGS', 'Toppings'),
        ('PACKAGING', 'Packaging'),
    ]
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    status = models.CharField(max_length=50, choices=[
        ('In Stock', 'In Stock'),
        ('Low Stock', 'Low Stock'),
        ('Out of Stock', 'Out of Stock')
    ])
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_name} ({self.category})"
