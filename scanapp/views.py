from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.db.models import Count
import datetime
from django.utils.timezone import now
from django.utils import timezone
from django.db.models import Sum, Count
from datetime import timedelta
from datetime import date
from datetime import datetime
from django.shortcuts import get_object_or_404
import json
from django.http import JsonResponse
from django.core.serializers import serialize
from django.forms.models import model_to_dict  # Use for more control
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.template.loader import render_to_string


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
    nextID = Status.objects.get(id=1)
    print(type(nextID.next_id))
    if product_id == 'N/A':
        
        context = {
            'nextID' : nextID.next_id,
        }
        return render(request, 'add_product.html',context)
        
    else:
        context = {
            'nextID' : nextID.next_id,
            'product_id': product_id
        }
        return render(request, 'add_product.html', context)
        

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
        # Recommend next number process for manual entry
        if ((int(product_id)/100000) < 1):
            nextID = Status.objects.get(id=1)
            step = nextID.next_id
            # Check if the next product_id is available
            while(True):
                nextProduct = Product.objects.filter(product_id = step).exists()
                # if the products exists add +1
                if nextProduct:
                    step +=1
                # else use the available id
                else:
                    nextID.next_id = step
                    nextID.save()
                    break
            
        

        return redirect('/search_for_product_page')

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
        
        product_id = request.POST['old_product_id']
        print(product_id)
        product = Product.objects.get(product_id=product_id)
        product.product_id= request.POST['product_id']
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
    now = datetime.now()
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
    print(f"Todays date: {today}")
    start_of_month = today.replace(day=1)
    print(f"Start date: {start_of_month}")
    end_of_month = today.replace(day=28) + timedelta(days=4)  # Ensures last day of the month
    print(f"End date: {end_of_month}")
    # Filter orders within the current month based on delivery_date
    orders_in_current_month = Order.objects.filter(
        delivery_date__gte=start_of_month,
        delivery_date__lte=end_of_month,
        order_type='Sell'
    )
    print(f"These are the orders in this month: {orders_in_current_month}")
    
    # Aggregate product data: name, number of orders, and total quantity for each product
    product_data = (OrderItem.objects
                    .filter(order__in=orders_in_current_month)
                    .values('product__name')  # Group by product name
                    .annotate(total_qty=Sum('quantity'), num_orders=Count('order', distinct=True))  # Sum of quantities, count of orders
                    .order_by('-total_qty')[:5])  # Order by total quantity, limit to 5
    print(f"These are the products: {product_data}")
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
    search_query = request.GET.get('search', '')
    
    if search_query:
        print(f"Search query: {search_query}")
        orders_cards = OrderCard.objects.select_related('order', 'delivery', 'order__customer') \
            .filter(order__customer__name__icontains=search_query) \
            .order_by('-order__delivery_date', '-id')
    else:
        print("No search query")
        orders_cards = OrderCard.objects.select_related('order', 'delivery', 'order__customer') \
            .order_by('-order__delivery_date', '-id')
        print(orders_cards)
    
    delivery = Delivery.objects.all()
    customers = Customer.objects.all()

    # Pagination
    paginator = Paginator(orders_cards, 20)  # Show 20 order cards per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(f"Page number: {page_number}")

    context = {
        'page_obj': page_obj,  # Use paginated orders_cards
        'delivery': delivery,
        'customers': customers,
    }
#   I want to add a code that checks if the request is an ajax request or not
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            print("This is an AJAX request")
            html = render_to_string('partials/order_cards.html', context, request=request)
            return JsonResponse({'data': html})
    print("This is not an AJAX request")
    print(context)
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
            'discount': str(item.discount),  # Convert Decimal to string for JSON serialization
            'total_price': str(item.total_items_price),  # Convert Decimal to string for JSON serialization
        }
        test.append(product_info)
    table_id = "table_" + str(orderID)
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

def order_page_assign_new_customer(request):
    if request.method == 'POST':
        '''
        Django expects data in request.POST when using application/json content-type.
        Django’s request.POST dictionary only works with application/x-www-form-urlencoded or multipart/form-data, so
        when using application/json, you need to parse the JSON data from the request body manually.
        '''
        data = json.loads(request.body)
        cardID = data.get("cardID")
        newCustomerID = data.get("newCustomerID")
        
        # print(f"CardID: {cardID} / NewDriverID: {newDriverID}")
        # Get card and driver instances
        card = get_object_or_404(OrderCard, id=cardID)
        new_customer = get_object_or_404(Customer, id=newCustomerID)
        # print(card)
        # print(new_driver.driver_name)
        # Assign new driver to card
        print(f"New customer is : {new_customer}")
        card.order.customer = new_customer
        card.order.save()
        # card.save()
        
    response_data = {
        'customer_name': card.order.customer.name,
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
        return redirect("orders_page")
# ----------- Create New Customer Page
def create_new_customer_page(request):
    return render(request, 'create_new_customer_page.html')

# ------------ Create New Customer Process

def create_new_customer_process(request):
    if request.method == "POST":
        customerName = request.POST.get("customer_name")
        customerPhone = request.POST.get("phone_number")
        customerEmail = request.POST.get("email")
        customerNote = request.POST.get("notes")
        customerAddress = request.POST.get("address")

        Customer.objects.create(
            name = customerName,
            phone_number = customerPhone,
            address = customerAddress,
            email = customerEmail,
            notes = customerNote,
        )
        return redirect("orders_page")
# ----------Edit Customer Page and Process----------------------------
def edit_customer_page(request, customerID):
    customer = get_object_or_404(Customer, id=customerID)
    context = {
        "customer": customer,
    }
    return render(request, 'edit_customer_page.html', context)

def edit_customer_process(request, customerID):
    # Retrieve the customer instance
    customer = get_object_or_404(Customer, id=customerID)
    
    # Handle GET request to render the edit page with customer data
    if request.method == "GET":
        return render(request, "edit_driver.html", {"customer": customer})
    
    # Handle POST request to update driver details
    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        email = request.POST.get("email","")
        notes = request.POST.get("notes", "")
        
        # Check if another driver with the same name already exists
        if Customer.objects.filter(name=customer_name).exclude(id=customerID).exists():
            messages.error(request, "A Customer with this name already exists. Please choose a unique name.")
            return render(request, "edit_driver.html", {"customer": customer})
        
        # Update driver details
        customer.name = customer_name
        customer.phone_number = phone_number
        customer.address = address
        customer.notes = notes
        customer.save()
        
        messages.success(request, "Customer details updated successfully!")
        return redirect("orders_dashboard_page")
    

def edit_order_card_page(request, order_card_id):
    # get the order card
    
    order_card = get_object_or_404(OrderCard, id=order_card_id)

    # get all the orders 
    
    available_orders = Order.objects.filter(display=True, order_card__isnull=True)
    orders = available_orders
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
    pre_order = Order.objects.get(id=request.POST['pre_order_id'])

    if request.method == 'POST':
        # Update fields based on form data

        order_card.delivery = Delivery.objects.get(id=int(request.POST.get('delivery'))) 
        order_card.order = Order.objects.get(id=int(request.POST.get('order'))) 
        order_card.total_discount = request.POST.get('total_discount')
        order_card.net_price = request.POST.get('net_price')
        order_card.order_notes = request.POST.get('order_notes')
        order_card.order.display = False
        order_card.save()

        pre_order.display = True
        pre_order.save()
        
        messages.success(request, "Order card updated successfully.")
        return redirect('orders_dashboard_page')  # Adjust to the actual success page


    return render(request, 'order_card_edit_page.html', {
        'order_card': order_card,
        'deliveries': deliveries,
        "orders" : orders,
        
    })


def create_new_order_card_page(request):
    # Fetch orders without an OrderCard and with display set to True
    available_orders = Order.objects.filter(display=True, order_card__isnull=True)
    deliveries = Delivery.objects.all()  # Fetch all deliveries for dropdown
    
    return render(request, 'create_new_order_card_page.html', {
        'available_orders': available_orders,
        'deliveries': deliveries,
    })



def create_new_order_card_process(request):
    
    if request.method == 'POST':
        order_id = request.POST.get('order')
        delivery_id = request.POST.get('delivery')
        total_discount = request.POST.get('total_discount')
        net_price = request.POST.get('net_price')
        order_notes = request.POST.get('order_notes')

        # Get order and delivery objects
        order = Order.objects.get(id=order_id)
        delivery = Delivery.objects.get(id=delivery_id) if delivery_id else None

        # Create and save new OrderCard
        order_card = OrderCard.objects.create(
            order=order,
            delivery=delivery,
            total_discount=total_discount,
            net_price=net_price,
            order_notes=order_notes,
        )
        # Mark the order as assigned
        order.display = False
        order.save()

        messages.success(request, "Order Card created successfully.")
        return redirect('orders_dashboard_page')  # Change to the relevant success page

    messages.error(request, "Failed to create Order Card.")
    return redirect('create_new_order_card_page')

def show_orders_page(request):
    orders = Order.objects.all()
    context = {
        'orders': orders,
        }

    return render(request, 'show_orders_page.html', context)


def SOP_process(request):
    if request.method == 'POST':
        # Retrieve or create the Customer instance
            customer_name = request.POST.get("customer_name")
            customer, created = Customer.objects.get_or_create(name=customer_name)


def sop_page(request):
    customer_names = Customer.objects.values_list('name', flat=True).distinct()
    products = Product.objects.all()
    # Get the time
    today = datetime.now().strftime("%Y-%m-%d")
    
    context = {
        'customers_names' : list(customer_names),
        'products' : products,
        'todaysDate' : today,
    }
    return render(request, 'sop_page.html', context)

def sop_page_request_product_data(request):
    if request.method == 'POST':
        selected_product_id = request.POST.get('selectedProductID')
        print("Received selectedProductID:", selected_product_id)  # Print to console
        product = Product.objects.get(product_id=selected_product_id)
        product_data = model_to_dict(product)
        return JsonResponse({'message': 'Product ID received', 'product': product_data})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def sop_sell_request(request):
    if request.method == 'POST':

        count = 1
        products_list = []
        customerName = request.POST.get('customerName')
        sellingDate = request.POST.get('sellingDate')
        # if the user didn't enter a customer name use N/A as default
        if not customerName:
            customerName = "N/A"
        customer, created = Customer.objects.get_or_create(name=customerName) # create or get customer
        print(customer.name)

        #----------------------------- CREATE NEW ORDER ----------------------------------------
# Customer Name : customer
# Order Type : "Sell"
# Delivery Date : "sellingDate"
# Status : "completed"
        # Create the Order with the Customer foreign key
        order = Order.objects.create(
            customer=customer,
            order_type="Sell",
            delivery_date=sellingDate,
            order_date=timezone.now(),
            status="completed"
        )
        print("Order created")

                #----------------------------- Loop to get the products details  ----------------------------------------
        # Loop to retrieve products dynamically
        
        while True:
            try:
                productName = request.POST.get(f'product_name_{count}')
                print(f"I am trying to get product_name_{count}")
                print(productName)
                if productName is None:
                    print("there is no data!!!")
                    break # Stop the loop if no more products
                
                # Retrieve product ID, quantity, and unit price
                productID = request.POST.get(f"product_id_{count}") # Get the ID
                productQTY = request.POST.get(f"product_qty_{count}") # Get the qty
                productPrice = request.POST.get(f"product_price_{count}") # get the price
                productDisc = request.POST.get(f"product_disc_{count}") # get the discount
                try:
                    totalDisc = request.POST.get("totalDisc") # get the total discount
                    print(f"Try is okay, and total Discount = {totalDisc}")
                except:
                    totalDisc = 0
                    print("I am at the expect")
                
                try:
                    totalPrice = request.POST.get("totalPrice") # get the total price
                except:
                    totalPrice = 0
                
                products_list.append(productName)
                print(f"Product List: {products_list}")
                print(f"Product ID: {productID}")
                print(f"Product qty: {productQTY}")
                print(f"Product price: {productPrice}")
                print(f"Total Discount: {totalDisc}")
                print(f"Total Price: {totalPrice}")
                print("-------------")
                


                # Create OrderItem if product and quantity exist
                if productID :
                    product = Product.objects.get(product_id=productID)
                    total_items_price = (int(productQTY) * float(productPrice)) - float(productDisc)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=int(productQTY),
                        price=float(productPrice),
                        discount=float(productDisc),
                        total_items_price=float(total_items_price),
                    )
                    product.inventory_qty = int(product.inventory_qty) - int(productQTY)
                    product.exported_qty = int(product.exported_qty) + int(productQTY)
                    product.save()
                count = count + 1
                print(f"OrderItem created for {product.name}")
            except Exception as e:
                print(f"Error: {e}, Breaking out of the loop")
                break

    
    #----------------------------- Create Order CARD  ----------------------------------------

        
        delivery_id = 7
        order_notes = "No notes yet"

        # Get order and delivery objects
        # order = Order.objects.get(id=order_id)
        delivery = Delivery.objects.get(id=delivery_id) if delivery_id else None

        # Check if there is a total discount or not
        try:
            totalDisc = request.POST.get("totalDisc") # get the total discount
            print(f"Try is okay, and total Discount = {totalDisc}")
        except:
            totalDisc = 0
            
        # check if there is a total price or not
        try:
            totalPrice = request.POST.get("totalPrice") # get the total price
        except:
            totalPrice = 0
        # Create and save new OrderCard
        order_card = OrderCard.objects.create(
            order=order,
            delivery=delivery,
            total_discount=totalDisc,
            net_price=totalPrice,
            order_notes=order_notes,
        )
        # Mark the order as assigned
        order.display = False
        order.save()

        return redirect ("sop_page")


# ------------------------------------------ Buy / Return page and process section

def sop_buy_page(request):
    customer_names = Customer.objects.values_list('name', flat=True).distinct()
    products = Product.objects.all()

        # Get the time
    today = datetime.now().strftime("%Y-%m-%d")
    
    context = {
        'customers_names' : list(customer_names),
        'products' : products,
        'todaysDate': today,
    }
    return render(request, 'sop_buy_page.html', context)

def sop_buy_request(request):
    if request.method == 'POST':

        count = 1
        products_list = []
        customerName = request.POST.get('customerName')
        buyingDate = request.POST.get('buyingDate')
        # if the user didn't enter a customer name use N/A as default
        if not customerName:
            customerName = "N/A"
        customer, created = Customer.objects.get_or_create(name=customerName) # create or get customer
        print(customer.name)

        #----------------------------- CREATE NEW ORDER ----------------------------------------
# Customer Name : customer
# Order Type : "Buy"
# Delivery Date : Now
# Status : "completed"
        # Create the Order with the Customer foreign key
        order = Order.objects.create(
            customer=customer,
            order_type="Buy",
            delivery_date=buyingDate,
            order_date=timezone.now(),
            status="completed"
        )
        print("Order created")

                #----------------------------- Loop to get the products details  ----------------------------------------
        # Loop to retrieve products dynamically
        while True:
            try:
                productName = request.POST.get(f'product_name_{count}')
                print(f"I am trying to get product_name_{count}")
                print(productName)
                if productName is None:
                    print("there is no data!!!")
                    break # Stop the loop if no more products
                
                # Retrieve product ID, quantity, and unit price
                productID = request.POST.get(f"product_id_{count}") # Get the ID
                productQTY = request.POST.get(f"product_qty_{count}") # Get the qty
                productPrice = request.POST.get(f"product_price_{count}") # get the price
                productDisc = request.POST.get(f"product_disc_{count}") # get the discount
                try:
                    totalDisc = request.POST.get("totalDisc") # get the total discount
                except:
                    totalDisc = 0
                
                try:
                    totalPrice = request.POST.get("totalPrice") # get the total price
                except:
                    totalPrice = 0
                
                products_list.append(productName)
                print(f"Product List: {products_list}")
                print(f"Product ID: {productID}")
                print(f"Product qty: {productQTY}")
                print(f"Product price: {productPrice}")
                print(f"Total Discount: {totalDisc}")
                print(f"Total Price: {totalPrice}")
                print("-------------")
                count += 1 


                # Create OrderItem if product and quantity exist
                
                product = Product.objects.get(product_id=productID)
                total_items_price = (int(productQTY) * float(productPrice)) - float(productDisc)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=int(productQTY),
                    price=float(productPrice),
                    discount=float(productDisc),
                    total_items_price=float(total_items_price),
                )
                product.inventory_qty = int(product.inventory_qty) + int(productQTY)
                product.imported_qty = int(product.imported_qty) + int(productQTY)
                product.save()
                print(f"OrderItem created for {product.name}")
            except Exception as e:
                print(f"Error: {e}, Breaking out of the loop")
                break

    
    #----------------------------- Create Order CARD  ----------------------------------------

        
        delivery_id = 7
        order_notes = "No notes yet"

        # Get order and delivery objects
        # order = Order.objects.get(id=order_id)
        delivery = Delivery.objects.get(id=delivery_id) if delivery_id else None

        # Create and save new OrderCard
        order_card = OrderCard.objects.create(
            order=order,
            delivery=delivery,
            total_discount=totalDisc,
            net_price=totalPrice,
            order_notes=order_notes,
        )
        print(f"OrderCard has been created: {order_card}")
        # Mark the order as assigned
        order.display = False
        order.save()

        return redirect ("sop_buy_page")



def inventory_page(request):
    products = Product.objects.all()
    context = {
        "data": "data",
        "products" : products,
    }
    return render (request, "inventory_page.html", context)


# This function will reset (inventory_qty / imported_qty and / exported_qty) in the database
# When running this function it will take sometime so don't worry about it if you think it froze
def reset_all_inv_qty(request):
    products = Product.objects.all()

    for product in products:
        
        product.inventory_qty = 0
        product.imported_qty = 0
        product.exported_qty = 0
        product.save()
        print(f"product: {product.name} QTY has been rested !!")
    return redirect ("inventory_page")



def edit_inventory_request(request):
    try:
        # Retrieve POST data
        productID = request.POST.get("formProductID")
        importedQty = request.POST.get("importedQty")
        exportedQty = request.POST.get("exportedQty")
        warningLimit = request.POST.get("setWarningLimit")

        # Validate inputs
        # if not all([productID, importedQty, exportedQty, abs(warningLimit)]):
        #     return JsonResponse({'error': 'All fields are required.'}, status=400)

        # if not (importedQty.isdigit() and exportedQty.isdigit() and warningLimit.isdigit()):
        #     return JsonResponse({'error': 'Quantities and warning limit must be valid integers.'}, status=400)

        # Retrieve product from the database
        product = Product.objects.get(product_id=productID)
        # print(f"Product retrieved: {product}")

        # Update product fields
        product.imported_qty = int(importedQty)
        product.exported_qty = int(exportedQty)
        product.inventory_qty = int(importedQty) - int(exportedQty)
        product.inventory_lower_limit = int(warningLimit)

        # Save changes
        product.save()

        return JsonResponse({
            'message': 'Product updated successfully',
            'product': {
                'product_id': product.product_id,
                'imported_qty': product.imported_qty,
                'exported_qty': product.exported_qty,
                'inventory_qty': product.inventory_qty,
                'inventory_lower_limit': product.inventory_lower_limit,
            }
        })
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Product not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)


def sop_edit_page(request,cardID):
    customer_names = Customer.objects.values_list('name', flat=True).distinct()
    products = Product.objects.all()
    card = OrderCard.objects.get(id = cardID)
    orderID = card.order.id
    orderItem = OrderItem.objects.filter(order_id=orderID)
    
    print(f"Order Items: {orderItem}")
    # Get the time
    today = datetime.now().strftime("%Y-%m-%d")
    
    context = {
        'customers_names' : list(customer_names),
        'products' : products,
        'todaysDate' : today,
        'card': card,
        'orderItem': orderItem,
    }
    return render(request, 'sop_edit_page.html', context)

def sop_edit_sell_request(request):
    if request.method == 'POST':
        cardID = request.POST.get('cardID')
        print(f"Card ID: {cardID}")
        card = OrderCard.objects.get(id=cardID)
        order = card.order
        customerEditName = request.POST.get('customerName')
        sellingDate = request.POST.get('sellingDate')
        #-------------------- The below section is responsible for updating the customer name in the order---------------------------------
        if customerEditName != card.order.customer.name:
            print(f"Customer name has been changed from {card.order.customer.name} to {customerEditName}")
        # if the user didn't enter a customer name use N/A as default
        if not customerEditName:
            customerEditName = "N/A" 
        # check if the new customer name exists or not
        customer, created = Customer.objects.get_or_create(name=customerEditName)
        card.order.customer = customer
        card.order.save()
        print(f"Customer name: {card.order.customer.name}")

        #-------------------- The below section is responsible for updating the delivery date in the order---------------------------------
        order.delivery_date = sellingDate
        order.save()
        print(f"Delivery Date: {order.delivery_date}")

        # ------------------------- Delete all the order items related to this order -------------------------
        count = 1
        print(f"I am trying to get product_name_{count}")
        productName = request.POST.get(f'product_name_{count}')
        print(productName)

        if productName is None:
            print("Please Make sure to add at least one product")
            return redirect('sop_edit_page', cardID=card.id)
        OrderItem.objects.filter(order=order).delete()  
        print("All order items have been deleted")
        #----------------------------- Loop to get the products details  ----------------------------------------
        
        while True:
            try:
                productName = request.POST.get(f'product_name_{count}')
                if productName is None:
                    print("there is no data left!!!")
                    break # Stop the loop if no more products
                
                # Retrieve product ID, quantity, and unit price
                productID = request.POST.get(f"product_id_{count}") # Get the ID
                productQTY = request.POST.get(f"product_qty_{count}") # Get the qty
                productPrice = request.POST.get(f"product_price_{count}") # get the price
                productDisc = request.POST.get(f"product_disc_{count}") # get the discount
                try:
                    totalDisc = request.POST.get("totalDisc") # get the total discount
                except:
                    totalDisc = 0
                
                try:
                    totalPrice = request.POST.get("totalPrice") # get the total price
                except:
                    totalPrice = 0
                
                print(f"Product ID: {productID}")
                print(f"Product qty: {productQTY}")
                print(f"Product price: {productPrice}")
                print(f"Total Discount: {totalDisc}")
                print(f"Total Price: {totalPrice}")
                print("-------------")
                count += 1 


                # Create OrderItem if product and quantity exist
                
                product = Product.objects.get(product_id=productID)
                print(f"Product: {product.name}")
                print("test")
                total_items_price = (int(productQTY) * float(productPrice)) - float(productDisc)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=int(productQTY),
                    price=float(productPrice),
                    discount=float(productDisc),
                    total_items_price=float(total_items_price),
                )
                # product.inventory_qty = int(product.inventory_qty) - int(productQTY)
                # product.exported_qty = int(product.exported_qty) + int(productQTY)
                # product.save()
                print(f"OrderItem created for {product.name}")
            except Exception as e:
                print(f"Error: {e}, Breaking out of the loop")
                break

        #----------------------------- Edit Create Order CARD net price and total discount ----------------------------------------
        # Check if there is a total discount or not
        try:
            totalDisc = request.POST.get("totalDisc") # get the total discount
            print(f"Try is okay, and total Discount = {totalDisc}")
        except:
            totalDisc = 0
            
        # check if there is a total price or not
        try:
            totalPrice = request.POST.get("totalPrice") # get the total price
        except:
            totalPrice = 0
        card.total_discount = totalDisc
        card.net_price = totalPrice
        print(f"Total Discount: {totalDisc}")
        print(f"Total Price: {totalPrice}")
        card.save()

        return redirect("sop_page")
# def sold_products_page(request):
#     products = Product.objects.all()
#     today = datetime.now().strftime("%Y-%m-%d")
#     context = {
#         "products" : products,
#         "today": today,
#     }
#     return render(request, "sold_products_page.html", context)

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
