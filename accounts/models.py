from django.db import models

class Log(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    product_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    action = models.CharField(max_length=100)
    staff = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product_name} - {self.action}"
