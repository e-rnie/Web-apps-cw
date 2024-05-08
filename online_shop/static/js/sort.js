document.addEventListener('DOMContentLoaded', function() {
    const sortBySelect = document.getElementById('sort-by');

    sortBySelect.addEventListener('change', function() {
        const selectedOption = sortBySelect.value;
        const productsContainer = document.querySelector('.products');
        const products = [...productsContainer.querySelectorAll('.product')];

        // Sort products based on selected option
        const sortedProducts = products.sort((a, b) => {
            let aValue = a.getAttribute(`data-${selectedOption}`);
            let bValue = b.getAttribute(`data-${selectedOption}`);

            // Handle different types of data for sorting
            if (selectedOption === 'name') {
                // Perform a case-insensitive comparison for names
                return aValue.toLowerCase().localeCompare(bValue.toLowerCase());
            } else {
                // Convert to float for numerical comparison
                return parseFloat(aValue) - parseFloat(bValue);
            }
        });

        // Remove existing products
        productsContainer.innerHTML = '';

        // Append sorted products
        sortedProducts.forEach(product => {
            productsContainer.appendChild(product);
        });
    });
});

