    document.addEventListener('DOMContentLoaded', function () {
        console.log("HI 1");
        const searchInput = document.getElementById('searchInput');
        const tableRows = document.querySelectorAll('#inventoryTable tbody tr');
                // Highlight rows with less than 10 products available
                tableRows.forEach(row => {
                    const availableQty = parseInt(row.querySelector('td:nth-child(7)').textContent, 10); // 7th column
                    if (!isNaN(availableQty) && availableQty < 10) {
                        row.style.backgroundColor = '#f8d7da'; // Light red background
                        row.style.color = '#842029'; // Dark red text
                    }
                });
                
        searchInput.addEventListener('input', function () {
            const searchTerm = searchInput.value.toLowerCase();
            

            tableRows.forEach(row => {
                // Get text content of the 'Product Name' and 'Category' columns
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

// Select modal and related elements
const modal = document.getElementById('editInventoryModal');
const modalTitle = document.getElementById('modalTitle');
const importedQty = document.getElementById('importedQty');
const exportedQty = document.getElementById('exportedQty');
const submitBtn = document.getElementById('submitBtn');
const cancelBtn = document.getElementById('cancelBtn');
const formProductID = document.getElementById('formProductID')

// Function to open the modal
function openModal(button) {
    // Extract data from button's data attributes
    const productID = button.getAttribute('data-productID');
    const productName = button.getAttribute('data-productName');
    const importedValue = button.getAttribute('data-importedQTY');
    const exportedValue = button.getAttribute('data-exportedQTY');
    
    // Set modal content
    console.log(modalTitle)
    modalTitle.childNodes[1].textContent = `(${productName})`;
    formProductID.value = productID;
    importedQty.value = importedValue || '';
    exportedQty.value = exportedValue || '';

    // Display modal
    modal.style.display = 'flex'; // Change to flex to apply centering
}

// Function to close the modal
function closeModal() {
    modal.style.display = 'none';
}

// Submit button action
submitBtn.addEventListener('click', function () {
    const importedValue = importedQty.value;
    const exportedValue = exportedQty.value;

    // Log the submitted data (or handle it as needed)
    console.log(`Submitted Imported: ${importedValue}, Exported: ${exportedValue}`);
    
    // Close modal after submission
    closeModal();
});

// Cancel button action
cancelBtn.addEventListener('click', closeModal);

// Close modal when clicking outside the content
window.addEventListener('click', function (event) {
    if (event.target === modal) {
        closeModal();
    }
});







