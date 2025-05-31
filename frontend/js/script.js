const API_BASE_URL = 'http://127.0.0.1:8000';

// Function to fetch all items from the backend
async function fetchAllItems() {
    try {
        // Careful about the trailing slash if the FastAPI route is defined as /items/
        const response = await fetch(`${API_BASE_URL}/items/`); 

        if (!response.ok) {
            // If the HTTP response status is not 200-299, throw an error
            throw new Error(`❌ HTTP error! status: ${response.status}`);
        }

        const items = await response.json();
        return items;
    } catch (error) {
        console.error('❌ Error fetching items:', error);
        // You could display an error message to the user here
        return []; // Return an empty array in case of error
    }
}

// Function to display items in the HTML list
function displayItems(items) {
    const itemsListUl = document.getElementById('items-list');
    if (!itemsListUl) {
        console.error('❌ Items list UL element not found!');
        return;
    }

    // Clear any existing items (e.g., the "Loading items..." message)
    itemsListUl.innerHTML = ''; 

    if (items.length === 0) {
        itemsListUl.innerHTML = '<li>No items found.</li>';
        return;
    }

    items.forEach(item => {
        const listItem = document.createElement('li');
        // Store the full item data as a dataset attribute for easy retrieval later
        listItem.dataset.itemId = item.id;
        listItem.dataset.itemName = item.name;
        listItem.dataset.itemDescription = item.description || '';  // Handle null description
        listItem.dataset.itemPrice = item.price;
        listItem.dataset.itemIsOffer = item.is_offer;

        listItem.innerHTML = `
            <strong>Name:</strong> ${item.name} <br>
            <strong>Price:</strong> $${item.price.toFixed(2)} <br>
            ${item.description ? `<strong>Description:</strong> ${item.description} <br>` : ''}
            ${item.is_offer ? `<strong>On Offer!</strong> <br>` : ''}
            <small>(ID: <span class="math-inline">\{item\.id\}\)</small\>
            <button class="edit-btn" data-id="{item.id}">Edit</button>
        `;
        // Add event listener for the new edit button
        const editButton = listItem.querySelector('.edit-btn');
        if (editButton) {
            editButton.addEventListener('click', () => {
                prepareEditForm(item);  // Pass the whole item object
            });
        }
        itemsListUl.appendChild(listItem);
    });
}

function prepareEditForm(item) {
    // Get the form and its elements
    const form = document.getElementById('create-item-form');
    const submitButton = form.querySelector('button[type="submit"]');
    const formTitle = document.querySelector('#item-creation-section h2');

    // Populate the form with the item's data
    form.name.value = item.name;
    form.description.value = item.description || '';  // Handle null description
    form.price.value = item.price;
    form.is_offer.checked = item.is_offer || false;  // Handle null/undefined is_offer

    // Store the ID of the item currently edited
    currentEditItemId = item.id;

    // Change UI to indicate "update mode"
    if (formTitle) {
        formTitle.textContent = 'Edit Item';
    }
    submitButton.textContent = 'Update Item';

    // Scroll to the form for better UX
    form.scrollIntoView({ behavior: 'smooth' });
}

// Function to handle the submission of the create item form
async function handleCreateItemFormSubmit(event) {
    event.preventDefault(); // Prevent the default form submission (which reloads the page)

    const form = event.target;
    const itemName = form.name.value;
    const itemDescription = form.description.value;
    const itemPrice = parseFloat(form.price.value); // Ensure price is a number
    const itemIsOffer = form.is_offer.checked; // Get boolean value from checkbox

    // Basic validation (more can be added)
    if (!itemName || isNaN(itemPrice) || itemPrice <= 0) {
        alert('⚠️ Please provide a valid name and a price greater than 0.');
        // In a real app, plan to show a nicer error message, not an alert.
        return;
    }

    const itemPayload = {
        name: itemName,
        description: itemDescription || null, // Send null if description is empty
        price: itemPrice,
        is_offer: itemIsOffer
    };

    try {
        const response = await fetch(`${API_BASE_URL}/items/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Tell the server we're sending JSON
            },
            body: JSON.stringify(itemPayload), // Convert the JS object to a JSON string
        });

        if (!response.ok) {
            // If the server responded with an error status (e.g., 422 for validation)
            const errorData = await response.json().catch(() => ({ detail: "Unknown error during item creation." }));
            throw new Error(`❌ HTTP error! status: ${response.status}, Message: ${errorData.detail || "No detail"}`);
        }

        const createdItem = await response.json();
        console.log('✅ Item created successfully:', createdItem);

        // Clear the form
        form.reset();

        // Refresh the list of items to show the new one
        initializePage(); // This will re-fetch and re-display all items

    } catch (error) {
        console.error('❌ Error creating item:', error);
        alert(`Error creating item: ${error.message}`); // Simple error feedback for the user
    }
}

// Main function to run when the page loads
async function initializePage() {
    const items = await fetchAllItems();
    displayItems(items);
}

// Add an event listener to run when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    initializePage(); // Fetch and display items on initial load

    // Get the form element and add the submit event listener
    const createItemForm = document.getElementById('create-item-form');
    if (createItemForm) {
        createItemForm.addEventListener('submit', handleCreateItemFormSubmit);
    } else {
        console.error('❌ Create item form not found!');
    }
});