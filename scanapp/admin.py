from django.contrib import admin
from .models import Product, Order, OrderItem, OrderHistory

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'customer_price', 'retail_price', 'category', 'display')
    search_fields = ('product_id', 'name', 'category')
    list_filter = ('category', 'display')
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
    list_display = ('id', 'customer_name', 'order_type', 'order_date', 'delivery_date', 'status', 'created_at', 'updated_at')
    search_fields = ('customer_name', 'status', 'order_type')
    list_filter = ('status', 'order_type', 'order_date', 'delivery_date')
    inlines = [OrderItemInline, OrderHistoryInline]

# Order History Admin
@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'timestamp')
    search_fields = ('order__customer_name', 'status')
    list_filter = ('status', 'timestamp')
    ordering = ('-timestamp',)

# Order Item Admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'display')
    search_fields = ('order__customer_name', 'product__name')
    list_filter = ('display',)
    ordering = ('order',)

