from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from dashboard.models import Notification


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
