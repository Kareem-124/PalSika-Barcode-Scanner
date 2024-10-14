from django.db import models

class Product(models.Model):
    product_id = models.CharField(max_length=13, unique=True)  # Barcode as Product ID
    name = models.CharField(max_length=100)
    customer_price = models.DecimalField(max_digits=10, decimal_places=2)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, default='N/A')  # New field

    def __str__(self):
        return f"{self.name} ({self.product_id})"
