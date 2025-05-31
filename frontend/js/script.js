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
        listItem.innerHTML = `
            <strong>Name:</strong> ${item.name} <br>
            <strong>Price:</strong> $${item.price.toFixed(2)} <br>
            ${item.description ? `<strong>Description:</strong> ${item.description} <br>` : ''}
            ${item.is_offer ? `<strong>On Offer!</strong> <br>` : ''}
            <small>(ID: ${item.id})</small>
        `;
        // Later, we can add update/delete buttons here:
        // listItem.innerHTML += ` <button onclick="editItem(${item.id})">Edit</button>`;
        // listItem.innerHTML += ` <button onclick="deleteItem(${item.id})">Delete</button>`;
        itemsListUl.appendChild(listItem);
    });
}

// Main function to run when the page loads
async function initializePage() {
    const items = await fetchAllItems();
    displayItems(items);
}

// Add an event listener to run initializePage when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', initializePage);