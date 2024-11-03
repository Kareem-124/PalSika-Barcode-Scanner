from django.db import models

class Product(models.Model):
    product_id = models.CharField(max_length=13, unique=True)  # Barcode as Product ID
    name = models.CharField(max_length=100)
    customer_price = models.DecimalField(max_digits=10, decimal_places=2)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, default='N/A')  # New field
    display = models.BooleanField(default=True)

class Customer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    display = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


# Orders Table
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('work_in_progress', 'Work In Progress'),
        ('canceled', 'Canceled')
    ]
    
    ORDER_TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell')
    ]
    
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES, default='SELLER')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', null=True)
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    display = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Order Items Table
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    display = models.BooleanField(default=True)

# Order History Table
class OrderHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='history')
    status = models.CharField(max_length=20, choices=Order.ORDER_STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    display = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.product_id})"
    
