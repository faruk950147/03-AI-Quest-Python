$(document).ready(function() {
    // CSRFToken
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    $('#search-input').on('keyup', function() {
        var term = $(this).val().trim();

        if(term.length > 0) {
            $.ajax({
                url: "/auto-searching-product/",
                method: 'GET',
                data: { term: term },
                success: function(res) {
                    var html = '';
                    if(res.length === 0) {
                        html = '<div class="list-group-item">No results found</div>';
                    } else {
                        res.forEach(function(item) {
                            html += `
                                <a href="${item.url}" class="list-group-item list-group-item-action d-flex align-items-center">
                                    <img src="${item.image}" style="width:40px; height:40px; object-fit:cover; margin-right:10px;" />
                                    <div>
                                        <div>${item.title}</div>
                                        <div>$${item.price}</div>
                                    </div>
                                </a>
                            `;
                        });
                    }
                    $('#autocomplete-display').html(html);
                },
                error: function(xhr, status, error) {
                    console.error("AJAX Error:", error);
                    alert("Something went wrong. Please try again.");
                }
            });
        } else {
            $('#autocomplete-display').empty();
        }
    });

    // Click outside dropdown to hide
    $(document).on('click', function(e) {
        if(!$(e.target).closest('#search-input, #autocomplete-display').length) {
            $('#autocomplete-display').empty();
        }
    });

    // ========================== For Shop Pages ===============================
    // Function to load products via AJAX
    function ajax_call(url) {
        $.ajax({
            url: url,
            type: 'GET',
            success: function(res) {
                $('#product-grid').html(res.html);
                $('#pagination').html(res.pagination_html);
            },
            error: function() {
                console.error("AJAX Error:", error);
                alert("Something went wrong. Please try again.");
            }
        });
    }

    // AJAX for pagination links
    $(document).on('click', '.page-link', function(e) {
        e.preventDefault();
        let url = $(this).attr('href');
        ajax_call(url);
    });

    // AJAX for per_page and sort select
    $('#per_page, #sort').on('change', function() {
        let per_page = $('#per_page').val();
        let sort = $('#sort').val();
        let url = window.location.pathname + `?per_page=${per_page}&sort=${sort}`;
        ajax_call(url);  
    });

    // Checkbox or price change triggers filter
    $('.filter-checkbox, #maxPrice').on('change', function(e) {
        e.preventDefault();
        let filter_object = {};
        // Gather all selected filters
        $('.filter-checkbox:checked').each(function () {
            let key = $(this).data('filter');
            let value = $(this).val();
            // Initialize array if not present
            if (!filter_object[key]) {
                filter_object[key] = [];
            }
            filter_object[key].push(value);
        });

        filter_object['maxPrice'] = $('#maxPrice').val();
        $('#priceValue').text('Max : ' + filter_object['maxPrice']);

        $.ajax({
            url: "/get-filter-products/",
            type: "POST",
            data: filter_object,
            headers: { 'X-CSRFToken': csrftoken },
            success: function(res) {
                $('#product-grid').html(res.html);
            }
        });
    });

    // All Filters — Select/Unselect all
    $("#all-filters").on('change', function() {
        let is_checked = $(this).is(":checked");
        $(".filter-checkbox").prop("checked", is_checked);
        $("#maxPrice").trigger("change");
    });
    // ============================= End Shop Pages ===========================

    // ============================ For Product Details Pages ==================================

    // ================== SIZE CHANGE ==================
    $(document).on('change', '.size-select', function (){
        let size_id = $(this).val();
        let product_id = $('#product_id').val(); 

        $.ajax({
            url: "/get-variant-by-size/",  
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            data: {
                size_id: size_id,
                product_id: product_id,
            },
            success: function (res) {
                $("#variant_id").val(res.variant_id);
                $('.colors-show').html(res.rendered_colors);
                $("#product-price").text(res.variant_price || '0');
                $("#display-color").text(res.color || '');
                $("#display-size").text(res.size || '');
                $("#variant-image").attr("src", res.variant_image);
                $("#display-variant-stock").text('Availability (Variant Stock): ' + (res.available_stock || 0));
                $("#sku").text(res.sku);

                bindColorEvents(); // color radio button bind
            },
            error: function (xhr) {
                console.error("AJAX Error:", error);
                alert("Something went wrong. Please try again.");
            }
        });
    });

    // ================== COLOR SELECT ==================
    function bindColorEvents() {
        $(document).off('change', 'input[name="variant_radio"]').on('change', 'input[name="variant_radio"]', function () {

            let variant_id = $(this).val();

            $.ajax({
                url: "/get-variant-by-color/",
                type: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
                data: {
                    variant_id: variant_id
                },
                success: function (res) {
                    $("#variant_id").val(res.variant_id);
                    $("#product-price").text(res.variant_price || '0');
                    $("#display-color").text(res.color || '');
                    $("#display-size").text(res.size || '');
                    $("#variant-image").attr("src", res.variant_image);
                    $("#sku").text(res.sku);
                    $("#display-variant-stock").text(
                        'Availability (Variant Stock): ' + (res.available_stock || 0)
                    );
                },
                error: function (xhr) {
                    console.error("AJAX Error:", error);
                    alert("Something went wrong. Please try again.");
                }
            });
        });
    }

    // Initial color binding
    bindColorEvents();

    // ================== REVIEW FORM ==================
    $('#review-form').on('submit', function (e) {
        e.preventDefault();

        let form = $(this);
        let data = new FormData(this);
        let btn = form.find('button[type="submit"]');

        let subject = $('#subject').val().trim();
        let comment = $('#comment').val().trim();
        let rating = $('input[name="rating"]:checked').val();

        if (!rating) {
            alertify.error("Please select a rating");
            return;
        }

        if (!subject || !comment) {
            alertify.error("Please fill in subject and comment");
            return;
        }

        data.append('rating', rating);
        btn.prop('disabled', true);

        $.ajax({
            url: "/product-review/",
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            data: data,
            processData: false,
            contentType: false,

            success: function (res) {
                if (res.status === 'success') {
                    alertify.success(res.message);
                    form[0].reset();
                    $('#review_count').text('Reviews (' + res.review_count + ')');
                    $('#reviews-items').prepend(res.review_html);
                } else {
                    alertify.error(res.message);
                }
            },

            error: function (xhr) {
                alertify.error("Something went wrong.");
                console.error(xhr.responseText);
            },

            complete: function () {
                btn.prop('disabled', false);
            }
        });
    });
    // ============================ For Product Details Pages ==================================


    // ============================ For Cart Pages ==================================
    // Add to Cart form submission via AJAX
    $("#cart-form").on("submit", function(e) {
        e.preventDefault();
        let formData = new FormData(this);

        $.ajax({
            url: "/cart/add-to-cart/",
            method: "POST",
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function(res) {
                if (res.status === "success") {
                    alertify.success(res.message);
                    $("#cart-form")[0].reset();  
                    $("#cart-count").text(res.cart_count);
                    $("#total-price").html('Your Cart:<br>' + res.subtotal + 'TK');
                } else {
                    alertify.error(res.message);
                }
            },
            error: function(xhr, status, error) {
                console.error("AJAX Error:", error);
                alert("Something went wrong. Please try again.");
            }
        });
    });

    // Quantity change (using event delegation)
    $(document).on('click', '.qty-btn', function () {
        let parent = $(this).closest('.cart-item');
        let cartId = parent.data('id');
        let action = $(this).data('action');

        $.ajax({
            url: "/cart/qty-inc-dec/",
            type: "POST",
            data: {
                cart_id: cartId,
                action: action,
                csrfmiddlewaretoken: csrftoken
            },
            success: function (res) {
                if (res.status === 'success') {
                    parent.find('#quantity').text(res.quantity);
                    parent.find("#item-total").text(parseFloat(res.item_total).toFixed(2) + ' TK');
                    $("#total-price").html('Your Cart:<br>' + parseFloat(res.subtotal).toFixed(2) + ' TK');
                    $('#sub-total').text(parseFloat(res.subtotal).toFixed(2) + ' TK');
                    $('#grand-total').text(parseFloat(res.grand_total).toFixed(2) + ' TK');

                    alertify.success(res.message);
                } else {
                    alertify.error(res.message);
                }
            },
            error: function (xhr, status, error) {
                console.error("AJAX Error:", error);
                alert("Something went wrong. Please try again.");
            }
        });
    });

    // Remove item
    $(document).on('click', '.remove-cart-item', function () {
        let btn = $(this);
        let parent = btn.closest('.cart-item'); // table row
        let cartId = parent.data('id');

        $.ajax({
            url: "/cart/cart-remove-item/",
            type: "POST",
            data: {
                cart_id: cartId,
                csrfmiddlewaretoken: csrftoken
            },
            success: function (res) {
                if (res.status === 'success') {
                    // Remove item row
                    parent.remove();
                    $("#cart-count").text(res.cart_count);
                    // Update totals
                    $("#total-price").html('Your Cart:<br>' + res.subtotal + ' TK');
                    $('#sub-total').text(parseFloat(res.subtotal).toFixed(2) + ' TK');
                    $('#grand-total').text(parseFloat(res.grand_total).toFixed(2) + ' TK');

                    // Show success message
                    alertify.success(res.message);
                } else {
                    alertify.error(res.message);
                }
            },
            error: function () {
                console.error("AJAX Error:", error);
                alert("Something went wrong. Please try again.");
            }
        });
    });

    // Add to wishlist 
    $(".add-to-wish").on("click", function(e) {
        e.preventDefault();
        let product_id = $(this).data("product_id");
        let variant_id = $(this).data("variant_id");
        console.log('product_id', product_id, 'variant_id', variant_id)

        $.ajax({
            url: "/cart/add-to-wish/",
            method: "POST",
            data: {
                product_id: product_id,
                variant_id: variant_id
            },
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function(res) {
                if (res.status === "added") {
                    alertify.success(res.message);
                    $("#wish-count").text(res.wish_count);
                } else if(res.status === "removed") {
                    alertify.error(res.message);
                    $("#wish-count").text(res.wish_count);
                }
            },
            error: function(xhr, status, error) {
                console.error("AJAX Error:", error);
                alert("Something went wrong. Please try again.");
            }
        });
    });

    // Remove item
    $(document).on('click', '.remove-wish-item', function () {
        let btn = $(this);
        let parent = btn.closest('.cart-item');  // table row
        let itemId = parent.data('id');

        $.ajax({
            url: "/cart/wish-remove-item/",  // wishlist 
            type: "POST",
            data: {
                wish_id: itemId,
                csrfmiddlewaretoken: csrftoken
            },
            success: function(res) {
                if (res.status === 'success') {
                    parent.remove();  // row remove
                    $("#wish-count").text(res.wish_count);  // wish count update
                    alertify.success(res.message);
                } else {
                    alertify.error(res.message);
                }
            },
            error: function(xhr, status, error) {
                console.error("AJAX Error:", error);
                alert("Something went wrong. Please try again.");
            }
        });
    });


    // ============================= For Cart Pages ===================================

    // ============================= For checkout Pages ===================================
    $('#apply-coupon-btn').on('click', function(e) {
        e.preventDefault();
        let data = { 'coupon_code': $('#coupon-code').val() };

        $.ajax({
            url: "/checkout/checkout/",  // CheckoutView post
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken }, // ensure csrftoken variable is set
            data: data,
            success: function(res){
                if(res.status === 'success'){
                    console.log(res)
                    $('#sub-total').text('Subtotal: ' + parseFloat(res.subtotal).toFixed(2) + ' TK');
                    $('#discount-amount').text('Discount: ' + parseFloat(res.discount_amount).toFixed(2) + ' TK');
                    $('#grand-total').text('Grand Total: ' + parseFloat(res.grand_total).toFixed(2) + ' TK');
                    alertify.success(res.message);
                } else {
                    alertify.error(res.message);
                }
            },
            error: function(xhr, status, error){
                console.error("AJAX Error:", error);
                alertify.error("Something went wrong. Please try again.");
            }
        });
    });

    $('#checkout-form').on('submit', function(e){
        e.preventDefault();
        let data = new FormData(this); // includes payment_method, address, coupon_code etc.

        $.ajax({
            url: "/checkout/checkout-place/", // CheckoutPlaceView
            method: 'POST',
            headers: { 'X-CSRFToken': '{{ csrf_token }}' },
            data: data,
            processData: false,
            contentType: false,
            success: function(res){
                if(res.status === 'success'){
                    alertify.success(res.message);
                    window.location.href = '/checkout/checkout-success/' + res.checkout_id + '/';
                } else {
                    alertify.error(res.message);
                }
            },
            error: function(xhr){
                alertify.error("Something went wrong during checkout.");
                console.error(xhr.responseText); // This helps debug 500 errors
            }
        });
    });    
    // ============================= For checkout Pages ===================================
});