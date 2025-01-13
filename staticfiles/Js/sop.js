var rowCount = 0;
const csrf = document.getElementsByName("csrfmiddlewaretoken");
// Add new product row
function addProduct() {
    // you need to get the csrf_token value and send it with the post 
    
    const selectedProductID = document.getElementById('modalProductSelect').value;
    const url = `../sop_page_request_product_data/`;
    // console.log(csrf[0].value);


    $.post(url,
    {
    'selectedProductID': selectedProductID,
    'csrfmiddlewaretoken': csrf[0].value
    },
    
    function(response){
        // console.log(response.product.customer_price);
        product = response.product;
        rowCount++;
        // console.log(rowCount);
        const tableBody = document.getElementById('product-table-body');
        const row = document.createElement('tr');
        row.setAttribute("onchange","reCalculate(this)");
        row.setAttribute("value",product.customer_price);
        
        row.innerHTML = `
            <td>${rowCount}</td>
            <input name="product_id_${rowCount}" type="hidden" value="${product.product_id}">
            <td ><input name="product_name_${rowCount}" type="text" class="form-control" placeholder="Product Name" value = "${product.name}"></td>
            <td><input name="product_qty_${rowCount}" type="number" class="form-control" placeholder="QTY" min="1" value = "1"></td>
            <td><input name="product_price_${rowCount}" type="number" class="form-control" placeholder="Price/Unit" step="0.01" value = "${product.customer_price}"></td>
            <td><input name="product_disc_${rowCount}" type="number" class="form-control" placeholder="Discount" step="0.01" value=0></td>
            <td name="product_total_${rowCount}" class="total-price-cell" value = "${product.customer_price}">${product.customer_price}</td>
            <td><button class="btn-delete" onClick = "removeRow(this)">Delete</button></td>
            

        `;
        tableBody.appendChild(row);

        totalValue();


    }); 
    
}


let customers = document.getElementById("available_customers_names");
customers = customers.innerText;
const customerJson = customers.replace(/'/g, '"');
customers = JSON.parse(customerJson);

// Function to handle customer search
function searchCustomers() {
const searchInput = document.getElementById("customerSearch").value.toLowerCase();
const resultsContainer = document.getElementById("customerResults");
resultsContainer.innerHTML = ""; // Clear previous results

if (searchInput.length === 0) {
    resultsContainer.style.display = "none";
    return;
}

// Filter customers and limit to top 5 results
const filteredCustomers = customers
    .filter(customer => customer.toLowerCase().includes(searchInput))
    .slice(0, 5);

// Display filtered results
if (filteredCustomers.length > 0) {
    filteredCustomers.forEach(customer => {
        const listItem = document.createElement("li");
        listItem.className = "list-group-item";
        listItem.textContent = customer;

        // Handle click event on search result
        listItem.addEventListener("click", () => {
            document.getElementById("customerSearch").value = customer;
            resultsContainer.style.display = "none"; // Hide results
        });

        resultsContainer.appendChild(listItem);
    });
    resultsContainer.style.display = "block"; // Show results
} else {
    resultsContainer.style.display = "none"; // Hide if no results
}
}





function searchProduct() {
    const input = document.getElementById('productsSearch').value.toLowerCase();
    const options = document.getElementById('modalProductSelect').options;

    for (let i = 0; i < options.length; i++) {
        const option = options[i];
        const text = option.textContent.toLowerCase();
        option.style.display = text.includes(input) ? 'block' : 'none';
    }
}

function reCalculate(e){
    // console.log(e.cells[2].firstChild.value); // QTY values
    // console.log(e.cells[3].firstChild.value); // Price values
    // console.log(e.cells[4].firstChild.value); // Discount values

    let qty = e.cells[2].firstChild.value;
    let price = e.cells[3].firstChild.value;
    let disc = e.cells[4].firstChild.value;

    total = (qty*price) - disc;
    // console.log(`the total price = ${total}`);
    e.setAttribute("value",total);
    e.cells[5].innerText = total;
    totalValue();
}

function totalValue(){
    let total = 0;
    let totalDisc = 0;
    let rows = document.getElementById("product-table-body");
    // console.log(rows.children.length);
    let rowsLength = rows.children.length;

    for (let i = 0; i < rowsLength; i++){
        // console.log(rows.children[i]);
        let totalElement = rows.children[i];
        let totalDiscElement = rows.children[i].cells[4].firstChild.value;
        // console.log(element);
        // console.log(element.getAttribute("value"));
        // Total Price
        price = parseInt(totalElement.getAttribute("value"));
        // console.log(`price = ${price}`);
        total = total + price;

        // total Discount
        // console.log(totalDiscElement);
        let disc = parseInt(totalDiscElement);
        // console.log(disc);
        totalDisc = totalDisc + disc;

    }
    let totalDiscount = document.getElementById("total-discount");
    let discountInputElement = document.getElementById("total-discount-input")
    let totalPriceInputElement = document.getElementById("total-price-input")
    let totalPrice = document.getElementById("total-price");

    totalDiscount.innerText = totalDisc;
    totalPrice.innerText = total;

    discountInputElement.value = totalDisc;
    totalPriceInputElement.value = total;
    // console.log(`Discount = ${totalDisc}`);

    // console.log(`total = ${total}`);
    return
}

function removeRow(button) {
    const row = button.parentElement.parentElement; // Get the <tr> containing the button
    row.remove();
    totalValue();
}



