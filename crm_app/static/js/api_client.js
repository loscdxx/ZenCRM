/**
 * CRM API Client
 * 
 * This file contains functions to interact with the CRM API endpoints.
 * It demonstrates how to fetch data from the backend and use it in the frontend.
 */

// Customer API Functions
const CustomerAPI = {
    /**
     * Get all customers
     * @returns {Promise} Promise that resolves to customer data
     */
    getAllCustomers: async function() {
        try {
            const response = await fetch('/api/customers');
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            return data.customers;
        } catch (error) {
            console.error('Error fetching customers:', error);
            throw error;
        }
    },
    
    /**
     * Get a specific customer by ID
     * @param {number} id - Customer ID
     * @returns {Promise} Promise that resolves to customer data
     */
    getCustomer: async function(id) {
        try {
            const response = await fetch(`/api/customers/${id}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            return data.customer;
        } catch (error) {
            console.error(`Error fetching customer ${id}:`, error);
            throw error;
        }
    },
    
    /**
     * Create a new customer
     * @param {Object} customerData - Customer data object
     * @returns {Promise} Promise that resolves to created customer data
     */
    createCustomer: async function(customerData) {
        try {
            const response = await fetch('/api/customers', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(customerData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error creating customer:', error);
            throw error;
        }
    },
    
    /**
     * Update an existing customer
     * @param {number} id - Customer ID
     * @param {Object} customerData - Updated customer data
     * @returns {Promise} Promise that resolves to updated customer data
     */
    updateCustomer: async function(id, customerData) {
        try {
            const response = await fetch(`/api/customers/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(customerData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error(`Error updating customer ${id}:`, error);
            throw error;
        }
    },
    
    /**
     * Delete a customer
     * @param {number} id - Customer ID
     * @returns {Promise} Promise that resolves to success message
     */
    deleteCustomer: async function(id) {
        try {
            const response = await fetch(`/api/customers/${id}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error(`Error deleting customer ${id}:`, error);
            throw error;
        }
    }
};

// Deal API Functions
const DealAPI = {
    /**
     * Get all deals
     * @returns {Promise} Promise that resolves to deal data
     */
    getAllDeals: async function() {
        try {
            const response = await fetch('/api/deals');
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            return data.deals;
        } catch (error) {
            console.error('Error fetching deals:', error);
            throw error;
        }
    },
    
    /**
     * Get a specific deal by ID
     * @param {number} id - Deal ID
     * @returns {Promise} Promise that resolves to deal data
     */
    getDeal: async function(id) {
        try {
            const response = await fetch(`/api/deals/${id}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            return data.deal;
        } catch (error) {
            console.error(`Error fetching deal ${id}:`, error);
            throw error;
        }
    },
    
    /**
     * Create a new deal
     * @param {Object} dealData - Deal data object
     * @returns {Promise} Promise that resolves to created deal data
     */
    createDeal: async function(dealData) {
        try {
            const response = await fetch('/api/deals', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dealData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error creating deal:', error);
            throw error;
        }
    },
    
    /**
     * Update an existing deal
     * @param {number} id - Deal ID
     * @param {Object} dealData - Updated deal data
     * @returns {Promise} Promise that resolves to updated deal data
     */
    updateDeal: async function(id, dealData) {
        try {
            const response = await fetch(`/api/deals/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dealData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error(`Error updating deal ${id}:`, error);
            throw error;
        }
    },
    
    /**
     * Delete a deal
     * @param {number} id - Deal ID
     * @returns {Promise} Promise that resolves to success message
     */
    deleteDeal: async function(id) {
        try {
            const response = await fetch(`/api/deals/${id}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error(`Error deleting deal ${id}:`, error);
            throw error;
        }
    }
};

// Example usage: Create a customer list component
class CustomerList {
    constructor(containerId) {
        this.containerId = containerId;
        this.customers = [];
        this.init();
    }
    
    async init() {
        try {
            // Fetch customers from API
            this.customers = await CustomerAPI.getAllCustomers();
            this.render();
            this.attachEventListeners();
        } catch (error) {
            console.error('Failed to initialize customer list:', error);
            document.getElementById(this.containerId).innerHTML = `
                <div class="alert alert-danger">
                    Failed to load customers. Please try again later.
                </div>
            `;
        }
    }
    
    render() {
        const container = document.getElementById(this.containerId);
        if (!container) return;
        
        // Create table HTML
        let html = `
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">Customers</h2>
                    <button id="add-customer-btn" class="btn btn-primary">
                        <i class="fas fa-user-plus"></i> Add Customer
                    </button>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Email</th>
                                    <th>Company</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
        `;
        
        // Add customer rows
        if (this.customers.length === 0) {
            html += `
                <tr>
                    <td colspan="5" class="text-center">No customers found</td>
                </tr>
            `;
        } else {
            this.customers.forEach(customer => {
                html += `
                    <tr data-customer-id="${customer.id}">
                        <td>${customer.name}</td>
                        <td>${customer.email}</td>
                        <td>${customer.company}</td>
                        <td>
                            <span class="badge badge-${this.getStatusClass(customer.status)}">
                                ${customer.status}
                            </span>
                        </td>
                        <td>
                            <div class="actions">
                                <button class="btn-icon view-customer" data-id="${customer.id}" title="View">
                                    <i class="fas fa-eye"></i>
                                </button>
                                <button class="btn-icon edit-customer" data-id="${customer.id}" title="Edit">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button class="btn-icon btn-icon-danger delete-customer" data-id="${customer.id}" title="Delete">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </td>
                    </tr>
                `;
            });
        }
        
        html += `
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }
    
    getStatusClass(status) {
        switch (status) {
            case 'Active': return 'success';
            case 'Pending': return 'warning';
            default: return 'info';
        }
    }
    
    attachEventListeners() {
        const container = document.getElementById(this.containerId);
        if (!container) return;
        
        // Add customer button
        const addButton = container.querySelector('#add-customer-btn');
        if (addButton) {
            addButton.addEventListener('click', () => {
                this.showCustomerForm();
            });
        }
        
        // View customer buttons
        const viewButtons = container.querySelectorAll('.view-customer');
        viewButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const customerId = e.currentTarget.getAttribute('data-id');
                window.location.href = `/customers/${customerId}`;
            });
        });
        
        // Edit customer buttons
        const editButtons = container.querySelectorAll('.edit-customer');
        editButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const customerId = e.currentTarget.getAttribute('data-id');
                this.editCustomer(customerId);
            });
        });
        
        // Delete customer buttons
        const deleteButtons = container.querySelectorAll('.delete-customer');
        deleteButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const customerId = e.currentTarget.getAttribute('data-id');
                this.deleteCustomer(customerId);
            });
        });
    }
    
    async deleteCustomer(id) {
        if (!confirm('Are you sure you want to delete this customer?')) {
            return;
        }
        
        try {
            await CustomerAPI.deleteCustomer(id);
            
            // Remove from local array
            this.customers = this.customers.filter(customer => customer.id !== parseInt(id));
            
            // Re-render the list
            this.render();
            this.attachEventListeners();
            
            // Show success message
            this.showNotification('Customer deleted successfully', 'success');
        } catch (error) {
            console.error('Error deleting customer:', error);
            this.showNotification('Failed to delete customer', 'danger');
        }
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} notification`;
        notification.innerHTML = message;
        
        // Add to document
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
    
    // Additional methods for handling forms, etc.
}

// Initialize components when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check if customer list container exists
    const customerListContainer = document.getElementById('customer-list-container');
    if (customerListContainer) {
        new CustomerList('customer-list-container');
    }
    
    // Add more component initializations as needed
});