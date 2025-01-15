// First get the table and count the number of rows it already have
// Then add a new row with the count + 1
var rowCount = 0;
document.addEventListener('DOMContentLoaded', (event) => {
    function addRow() {
        var table = document.getElementById("products-table");   
        rowCount = table.rows.length -1;
        console.log(rowCount);
    }
    addRow();
});


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
        row.setAttribute("value",product.product_id);
        
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
    console.log(`QTY = ${qty}`);
    let price = e.cells[3].firstChild.value;
    console.log(`Price = ${price}`);
    let disc = e.cells[4].firstChild.value;
    console.log(`Discount = ${disc}`);


    total = (qty*price) - disc;
    console.log(`the total price = ${total}`);
    e.cells[5].setAttribute("value",total); // set the value attribute of the cell to the 'total' value
    e.cells[5].innerText = total; // set the inner text of the cell to the 'total' value
    totalValue();
}

function totalValue() {
    let total = 0;
    let totalDisc = 0;
    let rows = document.getElementById("product-table-body");
    let rowsLength = rows.children.length;

    for (let i = 0; i < rowsLength; i++) {
        let totalElement = rows.children[i];
        totalElement = rows.children[i].cells[5]; // Get the total price cell
        let totalDiscElement = rows.children[i].cells[4].firstChild.value; // Get the discount cell value
        // console.log("TotalDisc Element value :"+totalDiscElement);
        // console.log(totalElement);
        // console.log(totalElement.getAttribute("value"));
        let price = parseInt(totalElement.getAttribute("value")); // Get the total price value (This step might be unnecessary as the value is already set in the cell as an integer)
        total = total + price;

        let disc = parseInt(totalDiscElement);
        totalDisc = totalDisc + disc;
    }
    let totalDiscount = document.getElementById("total-discount");
    let discountInputElement = document.getElementById("total-discount-input");
    // Update the total discount and total price elements
    totalDiscount.innerText = totalDisc;
    discountInputElement.value = totalDisc;

    let totalOfAllProductsElement = document.getElementById("total-price");
    let totalInputElement = document.getElementById("total-price-input");
    totalOfAllProductsElement.innerText = total;
    totalInputElement.value = total;
    // console.log("Total Discount: " + totalDisc);
    // console.log("Total Price: " + total);
    // console.log("Total Discount Element: ", totalDiscount);
    // console.log("Discount Input Element: ", discountInputElement);
    // console.log("Total Price Element: ", totalOfAllProductsElement);
}

function removeRow(button) {
    const row = button.parentElement.parentElement; // Get the <tr> containing the button
    row.remove();
    rowCount -= 1;
    totalValue();
}

document.addEventListener('DOMContentLoaded', (event) => {
    totalValue();
});


