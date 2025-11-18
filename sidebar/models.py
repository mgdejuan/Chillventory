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

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action_taken = models.CharField(max_length=20, choices=ACTION_CHOICES)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    stock_status = models.CharField(max_length=50, blank=True, null=True)
    date_and_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} - {self.action_taken} - {self.date_and_time.strftime('%Y-%m-%d %H:%M')}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.message[:50]}"
