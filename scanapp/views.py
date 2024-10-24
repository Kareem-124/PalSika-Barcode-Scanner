from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Product

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
    return render(request,'orders_dashboard.html' )



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
