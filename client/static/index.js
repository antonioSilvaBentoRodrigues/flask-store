const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll(".btn-outline-success").forEach(button => {
        button.onclick = function() {
            const productId = this.getAttribute('data-product-id');
            fetch('/add_product', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `product_id=${productId}`
            }).then(response => {
                if (response.ok) {
                    location.reload();  
                } else {
                    alert('Failed to add product to cart');
                }
            }).catch(error => {
                console.error('Error:', error);
            });
        };
    });

    document.querySelectorAll(".btn-outline-danger").forEach(button => {
        button.onclick = function() {
            const productId = this.getAttribute('data-product-id');
            fetch('/delete_product', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `product_id=${productId}`
            }).then(response => {
                if (response.ok) {
                    location.reload();  
                } else {
                    alert('Failed to remove product from cart');
                }
            }).catch(error => {
                console.error('Error:', error);
            });
        };
    });

    document.querySelector("#btn-clear-cart").onclick = function() {
        fetch('/clear_cart', {
            method: 'POST'
        }).then(response => {
            if (response.ok) {
                location.href = "{{ url_for('bp_views.market') }}"; 
            } else {
                alert('Failed to clear cart');
            }
        }).catch(error => {
            console.error('Error:', error);
        });
    };
});

