// AJAX format
// csrf: this will work for all
const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

// change url as fit
url = `../edit_inventory_request/`;

    $.ajax({
        type: "POST",
        url: url,
        data: {
            "formProductID": formProductID.value,
            "importedQty": importedQty.value,
            "exportedQty": exportedQty.value,
            "setWarningLimit": setWarningLimit.value,
            "csrfmiddlewaretoken": csrf_token, // Ensuring CSRF token is included
        },
        dataType: "json", // Specify expected response type
        success: function(response) {
            // Do what ever you want here.
        },
        error: function(xhr, status, error) {
            console.error("AJAX Error:", status, error);
            alert("An error occurred while updating the product.");
        }
    });

// Back End Example:
/* Python

def edit_inventory_request(request):
    try:
        # Retrieve POST data
        productID = request.POST.get("formProductID")
        importedQty = request.POST.get("importedQty")
        exportedQty = request.POST.get("exportedQty")
        warningLimit = request.POST.get("setWarningLimit")

        # Validate inputs
        if not all([productID, importedQty, exportedQty, warningLimit]):
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        if not (importedQty.isdigit() and exportedQty.isdigit() and warningLimit.isdigit()):
            return JsonResponse({'error': 'Quantities and warning limit must be valid integers.'}, status=400)

        # Retrieve product from the database
        product = Product.objects.get(product_id=productID)
        print(f"Product retrieved: {product}")

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
*/