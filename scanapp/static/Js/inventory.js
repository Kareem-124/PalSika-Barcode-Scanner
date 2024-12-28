    document.addEventListener('DOMContentLoaded', function () {
        
        const searchInput = document.getElementById('searchInput');
        const tableRows = document.querySelectorAll('#inventoryTable tbody tr');
                // Highlight rows with less than 10 products available
                tableRows.forEach(row => {
                    let lowerLimit = row.getAttribute("data-lowerLimit");
                    

                    const availableQty = parseInt(row.querySelector('td:nth-child(7)').textContent, 10); // 7th column
                    if (!isNaN(availableQty) && availableQty <= lowerLimit) {
                        // row.style.backgroundColor = '#f8d7da'; // Light red background
                        // row.style.color = '#842029'; // Dark red text
                        row.setAttribute("class","red");
                    }
                });

                
        searchInput.addEventListener('input', function () {
            const searchTerm = searchInput.value.toLowerCase();
            

            tableRows.forEach(row => {
                
                // Get text content of the ''Product ID', Product Name', 'Category', and 'lowerLimit' columns
                const productID = row.querySelector('td:nth-child(2)').textContent.toLowerCase(); // 3rd column
                const productName = row.querySelector('td:nth-child(3)').textContent.toLowerCase(); // 3rd column
                const category = row.querySelector('td:nth-child(4)').textContent.toLowerCase();    // 4th column

                // Check if the search term matches either the product name or the category
                if (productName.includes(searchTerm) || category.includes(searchTerm) || productID.includes(searchTerm)) {
                    row.style.display = ''; // Show row
                } else {
                    row.style.display = 'none'; // Hide row
                }
            });
        });
        
        const table = document.getElementById('inventoryTable');

        let selectedRow = null; // this is a flag for each row
        table.querySelectorAll('tbody tr').forEach(function(row){
            row.addEventListener('click',function(){
                // Make sure each <tr> element have a unique id in order for this to work
                rowID="Edit"+row.id;

                
                editButton = document.getElementById(rowID);
                if (selectedRow){
                    selectedRow.classList.remove('selected-row');
                    preEditButtonID = "Edit"+selectedRow.id;
                    preEditButton = document.getElementById(preEditButtonID);
                    preEditButton.style.display='none';
    
                }
    
                if (selectedRow === row){
                    selectedRow = null;
                    editButton.style.display='none'
                }
    
                else{
                    row.classList.add('selected-row');
                    selectedRow = row;
                    
                    editButton.style.display='block'
    
                }
            });
        });

    });

    function rowHighlightCheck(rowNumber,dataLimit){
        const searchInput = document.getElementById('searchInput');
        const tableRows = document.querySelectorAll('#inventoryTable tbody tr');
        // Highlight rows with less than 10 products available
        row = (tableRows[rowNumber-1]);
        console.log(row);
            let lowerLimit = dataLimit;
            
            const availableQty = parseInt(row.querySelector('td:nth-child(7)').textContent, 10); // 7th column
            if (!isNaN(availableQty) && availableQty <= lowerLimit) {
                // console.log("I must change to red");
                // row.style.backgroundColor = '#f8d7da'; // Light red background
                // row.style.color = '#842029'; // Dark red text
                row.setAttribute("class","red");
                // console.log(row);
            }
            else{
                row.removeAttribute("style");
                row.removeAttribute("class");
            }
            


}
// Select modal and related elements
const modal = document.getElementById('editInventoryModal');
const modalTitle = document.getElementById('modalTitle');
const importedQty = document.getElementById('importedQty');
const exportedQty = document.getElementById('exportedQty');
const submitBtn = document.getElementById('submitBtn');
const cancelBtn = document.getElementById('cancelBtn');
const formProductID = document.getElementById('formProductID')
const setWarningLimit = document.getElementById('setWarningLimit')

// Function to open the modal
function openModal(button) {
    // Extract data from button's data attributes
    const productID = button.getAttribute('data-productID');
    const productName = button.getAttribute('data-productName');
    const importedValue = button.getAttribute('data-importedQTY');
    const exportedValue = button.getAttribute('data-exportedQTY');
    const inventoryLimit = button.getAttribute('data-inventoryLimit');
    const rowNumber = button.getAttribute('data-rowNumber');
    
    // Set modal content
    // console.log(modalTitle)
    modalTitle.childNodes[1].textContent = `(${productName})`;
    formProductID.value = productID;
    importedQty.value = importedValue || '';
    exportedQty.value = exportedValue || '';
    setWarningLimit.value = inventoryLimit || '';
    submitBtn.value = rowNumber || '';

    // Display modal
    modal.style.display = 'flex'; // Change to flex to apply centering
}

// Function to close the modal
function closeModal() {
    modal.style.display = 'none';
}

// Submit button action
// submitBtn.addEventListener('click', function () {
//     const importedValue = importedQty.value;
//     const exportedValue = exportedQty.value;

//     // Log the submitted data (or handle it as needed)
//     console.log(`Submitted Imported: ${importedValue}, Exported: ${exportedValue}`);
    
//     // Close modal after submission
//     closeModal();
// });

// Cancel button action
cancelBtn.addEventListener('click', closeModal);

// Close modal when clicking outside the content
window.addEventListener('click', function (event) {
    if (event.target === modal) {
        closeModal();
    }
});


function submitModal(element){


    const rowNumber = document.getElementById("submitBtn").value;
    const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const importedQty = document.getElementById('importedQty');
    const exportedQty = document.getElementById('exportedQty');
    const formProductID = document.getElementById('formProductID'); // product ID
    const setWarningLimit = document.getElementById('setWarningLimit');// Lower Limit
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
            // console.log(`Row Number: ${rowNumber}`);
            // console.log("Response:", response);
            const dataLimit = response.product.inventory_lower_limit;
            document.getElementById(`limit_${rowNumber}`).innerText = dataLimit;
            const editButton = document.getElementById(`edit-btn-${rowNumber}`);
            editButton.setAttribute("data-inventoryLimit",dataLimit);
            rowHighlightCheck(rowNumber,dataLimit);
            closeModal();
        },
        error: function(xhr, status, error) {
            console.error("AJAX Error:", status, error);
            alert("An error occurred while updating the product.");
        }
    });
    
}





