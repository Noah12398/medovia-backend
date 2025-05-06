document.addEventListener("DOMContentLoaded", function () {
    const productGrid = document.getElementById("product-grid");
    const categoryFilters = document.getElementById("category-filters");
    const searchInput = document.getElementById("search-input");

    let products = [];
    let categories = new Set(["all"]); // Always have 'all'
    let selectedCategory = "all";

    // Fetch products
    fetch('/api/products')
        .then(response => response.json())
        .then(data => {
            products = data;
            extractCategories();
            renderCategories();
            renderProducts(products);
        })
        .catch(error => {
            console.error('Error fetching products:', error);
            productGrid.innerHTML = '<p>Error loading products.</p>';
        });

    function extractCategories() {
        products.forEach(product => {
            if (product.category) {
                categories.add(product.category.toLowerCase());
            }
        });
    }

    function renderCategories() {
        categoryFilters.innerHTML = ""; // Clear first
        categories.forEach(category => {
            const button = document.createElement("button");
            button.classList.add("category-btn");
            if (category === "all") button.classList.add("active");
            button.setAttribute("data-category", category);
            button.innerText = capitalize(category);
            button.addEventListener("click", () => {
                document.querySelectorAll('.category-btn').forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                selectedCategory = category;
                filterProducts();
            });
            categoryFilters.appendChild(button);
        });
    }

    function renderProducts(filteredProducts) {
        productGrid.innerHTML = "";
        if (filteredProducts.length === 0) {
            productGrid.innerHTML = "<p>No products found.</p>";
            return;
        }
        filteredProducts.forEach(product => {
            const div = document.createElement("div");
            div.classList.add("product");
            div.innerHTML = `
            
                <img src="${product.image_url}" alt="${product.name}" style="width: 150px; height: 150px;">
                <h3>${product.name}</h3>
                <p>${product.pack}</p>
                <p>₹${product.price.toFixed(2)}</p>
                <button class="add-to-cart" onclick="addToCart(${product.id})">
                    <img src="static/images/add-to-cart.png" alt="Add to Cart">
                </button>

            `;
            productGrid.appendChild(div);
        });
    }

    function filterProducts() {
        const searchTerm = searchInput.value.toLowerCase();
        let filtered = products.filter(product => {
            const matchCategory = (selectedCategory === "all") || (product.category.toLowerCase() === selectedCategory);
            const matchSearch = product.name.toLowerCase().includes(searchTerm);
            return matchCategory && matchSearch;
        });
        renderProducts(filtered);
    }

    searchInput.addEventListener("input", filterProducts);

    function capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
});

// Mock addToCart function
function addToCart(productId) {
    console.log("Added product to cart:", productId);
    const notification = document.getElementById("cart-notification");
    notification.style.display = "block";
    setTimeout(() => {
        notification.style.display = "none";
    }, 2000);
}
