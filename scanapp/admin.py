from django.contrib import admin
from .models import *

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'customer_price', 'retail_price', 'category', 'display')
    search_fields = ('product_id', 'name', 'category')
    list_filter = ('category', 'display')
    ordering = ('name',)

# Customer Admin
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'address', 'notes')  # Adjust fields as per your Customer model
    search_fields = ('name', 'email', 'phone_number')
    ordering = ('name',)

# Order Items Inline (to include in OrderAdmin)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

# Order History Inline (to include in OrderAdmin)
class OrderHistoryInline(admin.TabularInline):
    model = OrderHistory
    extra = 1

# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_type', 'order_date', 'delivery_date', 'status', 'created_at', 'updated_at')
    search_fields = ('customer__name', 'status', 'order_type')
    list_filter = ('status', 'order_type', 'order_date', 'delivery_date')
    inlines = [OrderItemInline, OrderHistoryInline]

# Order History Admin
@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'timestamp')
    search_fields = ('order__customer__name', 'status')
    list_filter = ('status', 'timestamp')
    ordering = ('-timestamp',)

# Order Item Admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'display')
    search_fields = ('order__customer__name', 'product__name')
    list_filter = ('display',)
    ordering = ('order',)

# Delivery Admin
@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('driver_name', 'driver_phone', 'driver_city_line', 'created_date', 'updated_date')
    search_fields = ('driver_name', 'driver_phone', 'driver_city_line')
    list_filter = ('created_date', 'updated_date')
    ordering = ('driver_name',)

# Order Card Admin
@admin.register(OrderCard)
class OrderCardAdmin(admin.ModelAdmin):
    list_display = ('order', 'delivery', 'total_discount','net_price','created_date', 'updated_date')
    search_fields = ('order__customer__name', 'delivery__driver_name')  # Assuming `Order` is linked to `Customer`
    list_filter = ('created_date', 'updated_date')
    ordering = ('-created_date',)
