from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.db.models import Count
import datetime
from django.utils.timezone import now
from django.utils import timezone
from django.db.models import Sum, Count
from datetime import timedelta
from django.shortcuts import get_object_or_404
import json

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
    first_five_customers = orders.values_list('customer__name', flat=True).distinct()[:5]
    
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
    
    return product_data

def create_new_order_page(request):
    products = Product.objects.all()
    customer_names = Customer.objects.values_list('name', flat=True).distinct()
    
    context = {
        'products': products,
        'customer_names': list(customer_names)
    }
    return render(request, 'create_new_order_page.html', context)

def create_new_order_process(request):
    # create_new_order.html
        if request.method == "POST":
            count = 1
            products_list = []

            customer_name = request.POST.get("customer_name")
            order_type = request.POST.get("order_type", "sell")
            delivery_date = request.POST.get("delivery_date")
            status = request.POST.get("status")

            # Retrieve or create the Customer instance
            customer, created = Customer.objects.get_or_create(name=customer_name)

            # Create the Order with the Customer foreign key
            order = Order.objects.create(
                customer=customer,
                order_type=order_type,
                delivery_date=delivery_date or None,
                order_date=timezone.now(),
                status=status
            )
            print("Order created")
            
            # Loop to retrieve products dynamically
            while True:
                try:
                    data_count = request.POST.get(f"product_{count}")
                    if data_count is None:
                        break # Stop the loop if no more products
                    
                    # Retrieve product ID, quantity, and unit price
                    product_id = request.POST.get(f"product_{count}") # Get the ID
                    quantity = request.POST.get(f"product_qty_{count}") # Get the qty
                    unit_price = request.POST.get(f"product_price_{count}") # get the price
                    products_list.append(data_count)
                    print(f"Product ID: {data_count}")
                    count += 1 

                    # Create OrderItem if product and quantity exist
                    if product_id and quantity:
                        product = Product.objects.get(product_id=product_id)
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=int(quantity),
                            price=float(unit_price)
                        )
                    print("OrderItem created")
                except Exception as e:
                    print(f"Error: {e}, Breaking out of the loop")
                    break

            # products = products_list
            # print(f"this is products {products}")
            # for index, product_data in enumerate(products):
            #     print("I am in the loop")
            #     product_id = request.POST.get(f"products[{index}][product_id]")
            #     quantity = request.POST.get(f"products[{index}][quantity]")
            #     unit_price = request.POST.get(f"products[{index}][price]")

            #     if product_id and quantity:
            #         product = Product.objects.get(product_id=product_id)
            #         OrderItem.objects.create(
            #             order=order,
            #             product=product,
            #             quantity=int(quantity),
            #             price=float(unit_price)
            #         )
            #         print("I created ORderItem")

            return redirect("orders_dashboard_page")  # Redirect to a success page

        return render(request, "create_new_order.html")
    

# Pager: orders_page displays all opened order cards 
def orders_page(request):
    orders_cards = OrderCard.objects.select_related('order', 'delivery', 'order__customer').order_by('-order__delivery_date')
    delivery = Delivery.objects.all()
    
    context = {
        'orders_cards': orders_cards,
        'delivery': delivery,
    }
    return render(request, 'orders_page.html', context)

# This section is responsible for providing the products for each card in orders_page it uses Ajax for this operation.
def order_page_products_request(request, orderID):
    order = Order.objects.get(id= orderID)
    order_items = OrderItem.objects.filter(order=order)
    print(order_items)
    test = []
    for item in order_items:
        product_info = {
            'product_id': item.product.product_id,
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': str(item.price),  # Convert Decimal to string for JSON serialization
        }
        test.append(product_info)
    table_id = "table_" + orderID
    data = {
        'products' : test,
        'table_id' : table_id,
    }
    return JsonResponse(data)


# Process: Change the assigned driver for the order in order card
def order_page_assign_new_driver(request):
    if request.method == 'POST':
        '''
        Django expects data in request.POST when using application/json content-type.
        Django’s request.POST dictionary only works with application/x-www-form-urlencoded or multipart/form-data, so
        when using application/json, you need to parse the JSON data from the request body manually.
        '''
        data = json.loads(request.body)
        cardID = data.get("cardID")
        newDriverID = data.get("newDriverID")
        
        # print(f"CardID: {cardID} / NewDriverID: {newDriverID}")
        # Get card and driver instances
        card = get_object_or_404(OrderCard, id=cardID)
        new_driver = get_object_or_404(Delivery, id=newDriverID)
        # print(card)
        # print(new_driver.driver_name)
        # Assign new driver to card
        card.delivery = new_driver
        card.save()
        
    response_data = {
        'driver_name': card.delivery.driver_name,
        'driver_city_line': card.delivery.driver_city_line,
        'driver_phone': card.delivery.driver_phone,
    }
    print(response_data)
    return JsonResponse(response_data)


def create_new_driver_page(request):
    return render(request, "create_new_driver_page.html")

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

def add_driver_process(request):
    if request.method == "POST":
        # Retrieve data from the form
        driver_name = request.POST.get("driver_name")
        driver_city_line = request.POST.get("city_line")
        driver_phone = request.POST.get("phone")
        notes = request.POST.get("notes", "")

                # Check if driver with this name already exists
        if Delivery.objects.filter(driver_name=driver_name).exists():
            # If driver exists, send an error message and return to the form page
            messages.error(request, "A driver with this name already exists. Please enter a unique driver name.")
            return render(request, "create_new_driver_page.html", {
                "driver_name": driver_name,
                "driver_city_line": driver_city_line,
                "driver_phone": driver_phone,
                "notes": notes,
            })
        
        # Create a new Delivery entry
        new_driver = Delivery(
            driver_name=driver_name,
            driver_city_line=driver_city_line,
            driver_phone=driver_phone,
            notes=notes
        )
        new_driver.save()  # Save the new driver to the database

        # Success message and redirect
        messages.success(request, "New driver added successfully!")
        return redirect("orders_dashboard_page") 

    # If not a POST request, return to the form page
    return render(request, "create_new_driver_page.html")

def edit_driver_page(request, driver_id):
    driver = get_object_or_404(Delivery, id=driver_id)
    context = {
        "driver": driver,
    }
    return render(request, 'edit_driver_page.html', context)

def edit_driver_process(request, driver_id):
    # Retrieve the driver instance
    driver = get_object_or_404(Delivery, id=driver_id)
    
    # Handle GET request to render the edit page with driver data
    if request.method == "GET":
        return render(request, "edit_driver.html", {"driver": driver})
    
    # Handle POST request to update driver details
    if request.method == "POST":
        driver_name = request.POST.get("driver_name")
        driver_city_line = request.POST.get("city_line")
        driver_phone = request.POST.get("phone")
        notes = request.POST.get("notes", "")
        
        # Check if another driver with the same name already exists
        if Delivery.objects.filter(driver_name=driver_name).exclude(id=driver_id).exists():
            messages.error(request, "A driver with this name already exists. Please choose a unique name.")
            return render(request, "edit_driver.html", {"driver": driver})
        
        # Update driver details
        driver.driver_name = driver_name
        driver.driver_city_line = driver_city_line
        driver.driver_phone = driver_phone
        driver.notes = notes
        driver.save()
        
        messages.success(request, "Driver details updated successfully!")
        return redirect("orders_dashboard_page")
    
def edit_order_card_page(request, order_card_id):
    # get the order card
    order_card = get_object_or_404(OrderCard, id=order_card_id)

    # get all the orders 
    orders = Order.objects.all()
    
    # get all the drivers
    deliveries = Delivery.objects.all()

    context = {
        "order_card" : order_card,
        "orders" : orders,
        "deliveries" : deliveries,
        
    }

    return render(request, 'edit_order_card_page.html', context)

def edit_order_card_process(request, order_card_id):
    order_card = get_object_or_404(OrderCard, id=order_card_id)
    print(f"This is the order card object: {order_card.delivery}")
    deliveries = Delivery.objects.all()  # Retrieve all drivers for dropdown
            # get all the orders 
    orders = Order.objects.all()

    if request.method == 'POST':
        # Update fields based on form data
        print(Delivery.objects.get(id=int(request.POST.get('delivery'))))
        order_card.delivery = Delivery.objects.get(id=int(request.POST.get('delivery'))) 
        order_card.order = Order.objects.get(id=int(request.POST.get('order'))) 
        order_card.total_discount = request.POST.get('total_discount')
        order_card.net_price = request.POST.get('net_price')
        order_card.order_notes = request.POST.get('order_notes')
        order_card.save()
        messages.success(request, "Order card updated successfully.")
        return redirect('orders_dashboard_page')  # Adjust to the actual success page


    return render(request, 'order_card_edit_page.html', {
        'order_card': order_card,
        'deliveries': deliveries,
        "orders" : orders,
        
    })

def SOP_process(request):
    if request.method == 'POST':
        # Retrieve or create the Customer instance
            customer_name = request.POST.get("customer_name")
            customer, created = Customer.objects.get_or_create(name=customer_name)
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
