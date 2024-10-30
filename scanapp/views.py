from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.db.models import Count
import datetime
from django.utils.timezone import now
from django.utils import timezone

from django.db.models import Sum, Count
from datetime import timedelta


def index(request):
    return render(request, 'index.html')

def scan_barcode(request, code):
    try:
        product = Product.objects.get(product_id=code)
        return JsonResponse({
            "name": product.name,
            "customer_price": product.customer_price,
            "retail_price": product.retail_price,
            "notes": product.notes
        })
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found", "product_id": code}, status=404)

def add_product_page(request, product_id='N/A'):
    if product_id == 'N/A':
        return render(request, 'add_product.html')
        
    else:
        return render(request, 'add_product.html', {'product_id': product_id})
        

# Process: Adding new Product
def add_product(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        name = request.POST['name']
        customer_price = request.POST['customer_price']
        retail_price = request.POST['retail_price']
        category = request.POST['category']
        notes = request.POST['notes']

        Product.objects.create(
            product_id=product_id,
            name=name,
            customer_price=customer_price,
            retail_price=retail_price,
            category = category,
            notes=notes,
        )
        return redirect('/')

# Render Edit Product Page 'edit_product.html'
def edit_product_page(request,product_id):
    product = Product.objects.get(product_id=product_id)
    context ={
        'product_id': product_id,
        'product_name': product.name,
        'customer_price': product.customer_price,
        'retail_price': product.retail_price,
        'category' : product.category,
        'notes': product.notes,

    }
    return render(request, 'edit_product.html', context)

# Process: Edit the product
def edit_product_process(request):
    if request.method == 'POST':
        
        product_id = request.POST['product_id']
        product = Product.objects.get(product_id=product_id)
        
        product.name = request.POST['name']
        product.customer_price = request.POST['customer_price']
        product.retail_price = request.POST['retail_price']
        product.category = request.POST['category']
        product.notes = request.POST['notes']
        product.save()
        print(f"Product ${product.name} has been edited successfully.")
        return redirect('/search_for_product_page')
    
def search_for_product_page(request):
    products = Product.objects.all()
    context = {
        'products' : products, 
    }
    return render(request, 'search_for_product.html',context)

def orders_dashboard_page(request):
    total_orders = get_all_orders()
    total_orders_this_month = get_orders_for_current_month()
    total_orders_for_today = get_orders_for_today()
    total_pending_orders_by_delivery_date = get_pending_orders_by_delivery_date()
    top_products_for_current_month = get_top_products_for_current_month()
    context = {
        'total_orders' : total_orders,
        'total_orders_this_month' : total_orders_this_month,
        'total_pending_orders_by_delivery_date' : total_pending_orders_by_delivery_date,
        'total_orders_for_today' : total_orders_for_today['all_statuses'],
        'first_five_customers' : total_orders_for_today['first_five_customers'],
        'top_products_for_current_month' : top_products_for_current_month
    }
    return render(request,'orders_dashboard.html', context )

def get_all_orders():

    all_statuses = {
        'pending': 0,
        'completed': 0,
        'on_hold': 0,
        'work_in_progress': 0,
        'canceled': 0
    }
    
    # Group by status and count each status
    orders_count = Order.objects.values('status').annotate(count=Count('status'))

    for status in orders_count:
        all_statuses[status['status']] = status['count']

    return all_statuses 


def get_orders_for_current_month():
    # Get the current month and year
    now = datetime.datetime.now()
    current_year = now.year
    current_month = now.month

    all_statuses = {
        'pending': 0,
        'completed': 0,
        'on_hold': 0,
        'work_in_progress': 0,
        'canceled': 0
    }
    

    # Filter orders by the current month and year using the delivery_date
    orders = Order.objects.filter(delivery_date__year=current_year, delivery_date__month=current_month)

    # Group by status and count each status
    orders_count = orders.values('status').annotate(count=Count('status'))

    # Update the dictionary with the actual counts
    for status in orders_count:
        all_statuses[status['status']] = status['count']

    return all_statuses

def get_orders_for_today():
    today = now().date()  # Get the current date

    all_statuses = {
        'pending': 0,
        'completed': 0,
        'on_hold': 0,
        'work_in_progress': 0,
        'canceled': 0
    }
    
    # Filter orders with delivery_date equal to today's date
    orders = Order.objects.filter(delivery_date=today)
    
    # Count orders by status
    status_counts = orders.values('status').annotate(count=Count('status'))
    
    # Update the dictionary with the actual counts
    for status in status_counts:
        all_statuses[status['status']] = status['count']

    # Get the first 5 customer names
    first_five_customers = orders.values_list('customer_name', flat=True)[:5]
    
    return {
        'first_five_customers' : first_five_customers, 
        'all_statuses' : all_statuses,
    } 



def get_pending_orders_by_delivery_date():
    # Get today's date
    today = timezone.now().date()

    # Filter orders with status 'pending'
    pending_orders = Order.objects.filter(status='pending')

    # Separate orders into the three groups based on delivery date
    overdue_orders = pending_orders.filter(delivery_date__lt=today)
    today_orders = pending_orders.filter(delivery_date=today)
    future_orders = pending_orders.filter(delivery_date__gt=today)

    # Count each group
    pending_orders_by_date = {
        'overdue': overdue_orders.count(),
        'today': today_orders.count(),
        'future': future_orders.count()
    }

    return pending_orders_by_date


def get_top_products_for_current_month():
    # Get the current month
    today = now().date()
    start_of_month = today.replace(day=1)
    end_of_month = today.replace(day=28) + timedelta(days=4)  # Ensures last day of the month

    # Filter orders within the current month based on delivery_date
    orders_in_current_month = Order.objects.filter(
        delivery_date__gte=start_of_month,
        delivery_date__lte=end_of_month
    )
    
    # Aggregate product data: name, number of orders, and total quantity for each product
    product_data = (OrderItem.objects
                    .filter(order__in=orders_in_current_month)
                    .values('product__name')  # Group by product name
                    .annotate(total_qty=Sum('quantity'), num_orders=Count('order', distinct=True))  # Sum of quantities, count of orders
                    .order_by('-total_qty')[:5])  # Order by total quantity, limit to 5
    print(f"Product data: {product_data}")
    return product_data

# # Process: Delete
# def remove_order_list(request,order_id):
#     order_list = Order_list.objects.get(id=order_id)
#     order_list.delete()
#     return JsonResponse({'message': 'Success'})


# def edit_product_page(request, product_id):
#     product = Product.objects.get(id=product_id)
#     # Get all categories
#     categories = Category.objects.all()
#     # Navbar Selection page to bold it
#     selection = clear_selection()
#     selection['products'] = "selected"
#     # Check User session
#     user_session = check_session(request)
#     print(product.categories.cat_name)
#     context = {
#         'user_session': user_session,
#         'product': product,
#         'selection': selection,
#         'categories': categories,
#     }
#     return render(request, 'edit_product.html', context)
