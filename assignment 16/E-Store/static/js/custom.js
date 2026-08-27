console.log("Custom JS loaded " + window.location.host);
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
                url: "/auto/searching/product/",
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
            url: "/get/filter/products/",
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

    // SIZE CHANGE
    $(document).on('click', '.size-option', function () {

        let size_id = $(this).data('size-id');
        let product_id = $('#product-id').val();

        // Selected size
        $('.size-option').removeClass('active');
        $(this).addClass('active');

        // Reset selected variant
        $('#variant-id').val('');

        $.ajax({
            url: "/get/variant/by/size/",
            type: "POST",

            headers: {'X-CSRFToken': csrftoken},

            data: {
                size_id: size_id,
                product_id: product_id
            },

            success: function (res) {
                $('#color-options').html(res.rendered_colors);

                $("#product-stock").text(res.available_stock || '0');

                $("#product-price").text(res.variant_price || '0.0');

                $("#product-size").text(res.size || 'None');

                $("#product-color").text(res.color || 'None');

                $("#product-sku").text(res.sku || 'None');

                $("#variant-image").attr("src", res.variant_image);

                alertify.success("You have change variants")
                
                bindColorEvents();
            },

            error: function (xhr) {
                console.log("Size AJAX Error:", xhr.status, xhr.responseText);

                $('#color-options').html('');
                $('#variant-id').val('');

                alertify.error("Unable to load colors. Please try again.");
            }
        });
    });

    // COLOR SELECT
    function bindColorEvents() {
        $(document).off('click', '.color-option').on('click', '.color-option', function () {
            let variant_id = $(this).data('variant-id');

            if (!variant_id) {
                alertify.error("Please before select a size than color selected");
                return;
            }

            // Selected color
            $('.color-option').removeClass('active');
            $(this).addClass('active');

            $.ajax({
                url: "/get/variant/by/color/",
                type: "POST",

                headers: {'X-CSRFToken': csrftoken},

                data: {variant_id: variant_id},

                success: function (res) {
                    $('#variant-id').val(res.variant_id);

                    $("#product-stock").text(res.available_stock || '0');

                    $("#product-price").text(res.variant_price || '0.0');

                    $("#product-size").text(res.size || 'None');

                    $("#product-color").text(res.color || 'None');

                    $("#product-sku").text(res.sku || 'None');

                    $("#variant-image").attr("src", res.variant_image);
                    
                    alertify.success("You have change variants")
                },

                error: function (xhr) {
                    console.error("Color AJAX Error:", xhr.status, xhr.responseText);
                    $('#variant-id').val('');

                    alert("Unable to select this color. Please try again.");
                }
            });
        });
    }

    // INITIAL COLOR BINDING 
    bindColorEvents();

    // REVIEW FORM
    $('#review-form').on('submit', function (e) {
        e.preventDefault();

        let form = $(this);
        let data = new FormData(this);
        let btn = form.find('button[type="submit"]');

        let subject = ($('#id_subject').val() || '').trim();
        let comment = ($('#id_comment').val() || '').trim();
        let rating = $('input[name="rating"]:checked').val() || '';

        // =========================
        // Client-side validation
        // =========================
        if (!rating) {
            alertify.error('Please select a rating.');
            return;
        }

        if (!subject) {
            alertify.error('Please enter a subject.');
            return;
        }

        if (!comment) {
            alertify.error('Please enter a comment.');
            return;
        }

        // =========================
        // Disable submit button
        // =========================
        btn.prop('disabled', true);

        // =========================
        // AJAX request
        // =========================
        $.ajax({
            url: "/product/review/",
            type: "POST",

            headers: {
                "X-CSRFToken": csrftoken
            },

            data: data,
            processData: false,
            contentType: false,

            success: function (res) {
                if (res.status === "success") {
                    alertify.success(res.message);
                    // Reset form
                    form[0].reset();

                    // Update review count
                    $('#review-count').text('Reviews (' + res.review_count + ')');

                    // Add new review at the top
                    $('#reviews-items').prepend(res.review_html);

                } else {alertify.error(res.message || 'Unable to submit review.');}},

            error: function (xhr) {
                console.error('Review submission error:', xhr.responseText);

                if (xhr.responseJSON) {
                    alertify.error(xhr.responseJSON.message || 'Please correct the errors.');

                } else {alertify.error('Something went wrong.')}},

            complete: function () {btn.prop('disabled', false)}
        });
    });
    // ============================ For Product Details Pages ==================================


    // ============================ For Cart Pages ==================================
    // Add to Cart form submission via AJAX
    $("#cart-form").on("submit", function(e) {
        e.preventDefault();
        let formData = new FormData(this);

        $.ajax({
            url: "/cart/add/to/",
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
            url: "/cart/quantity/inc-dec/",
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
                    $("#total-price").html(parseFloat(res.subtotal).toFixed(2) + ' TK');
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
            url: "/cart/remove/view/",
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
                    $("#total-price").html(res.subtotal + ' TK');
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

    // Add / Toggle Wishlist

    $(".add-to-wish").on("click", function (e) {

        e.preventDefault();

        let product_id = $(this).data("product-id");
        let product_slug = $(this).data("product-slug");

        $.ajax({
            url: "/cart/wishlist/view/",
            method: "POST",
            data: {
                product_id: product_id,
                product_slug: product_slug
            },
            headers: {"X-CSRFToken": csrftoken},

            success: function (res) {
                if (res.status === "added") {
                    alertify.success(res.message);
                    $("#wish-count").text(res.wish_count);

                } else if (res.status === "removed") {
                    alertify.error(res.message);
                    $("#wish-count").text(res.wish_count);
                }
            },

            error: function (xhr, status, error) {
                console.error("AJAX Error:", error);
                console.error(xhr.responseText);

                alertify.error("Something went wrong. Please try again.");
            }
        });
    });

    // Remove Wishlist Item
    $(document).on("click", ".remove-wishlist-item", function (e) {

        e.preventDefault();

        let btn = $(this);
        let parent = btn.closest(".wishlist-item");
        let itemId = parent.data("id");

        $.ajax({
            url: "/cart/wishlist/remove/view/",
            type: "POST",

            data: {
                wish_id: itemId
            },

            headers: {
                "X-CSRFToken": csrftoken
            },

            success: function (res) {

                if (res.status === "success") {

                    parent.remove();

                    $("#wish-count").text(res.wish_count);

                    alertify.success(res.message);

                } else {

                    alertify.error(
                        res.message || "Unable to remove item."
                    );
                }
            },

            error: function (xhr, status, error) {

                console.error("AJAX Error:", error);
                console.error(xhr.responseText);

                alertify.error(
                    "Something went wrong. Please try again."
                );
            }
        });

    });

    // ============================= For Cart Pages ===================================

    // ============================= For checkout Pages ===================================
    // Apply Coupon AJAX
    $('#apply-coupon-btn').on('click', function(e) {
        e.preventDefault();
        
        let csrftoken = $('[name=csrfmiddlewaretoken]').val();
        let couponCode = $('#coupon-code').val();

        if(!couponCode){
            if (typeof alertify !== 'undefined') alertify.error("Please enter a coupon code.");
            else alert("Please enter a coupon code.");
            return;
        }

        $.ajax({
            url: '/checkout/view/', 
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            data: { 'coupon_code': couponCode },
            success: function(res){
                if(res.status === 'success'){
                    $('#sub-total').text('Subtotal: ' + parseFloat(res.subtotal).toFixed(2) + ' TK');
                    $('#discount-amount').text('Discount: ' + parseFloat(res.discount_amount).toFixed(2) + ' TK');
                    $('#grand-total').text('Grand Total: ' + parseFloat(res.grand_total).toFixed(2) + ' TK');
                    if (typeof alertify !== 'undefined') alertify.success(res.message);
                    else alert(res.message);
                } else {
                    if (typeof alertify !== 'undefined') alertify.error(res.message);
                    else alert(res.message);
                }
            },
            error: function(xhr, status, error){
                console.error("AJAX Error:", error);
                alert("Something went wrong applying the coupon. Please try again.");
            }
        });
    });

    // Submit Checkout Form AJAX
    $('#checkout-form').on('submit', function(e) {
        e.preventDefault();

        let data = new FormData(this);

        $.ajax({
            url: "/checkout/place/",
            method: "POST",

            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },

            data: data,
            processData: false,
            contentType: false,

            success: function(res) {

                if (res.status === "success") {

                    if (typeof alertify !== "undefined") {
                        alertify.success(res.message);
                    }

                    let successUrl = $("#checkout-config")
                        .data("success-url");

                    successUrl = successUrl.replace(
                        "/0/",
                        "/" + res.checkout_id + "/"
                    );

                    window.location.href = successUrl;

                } else {

                    if (typeof alertify !== "undefined") {
                        alertify.error(res.message);
                    } else {
                        alert(res.message);
                    }
                }
            },

            error: function(xhr) {
                alert("Something went wrong during checkout.");
                console.error(xhr.responseText);
            }
        });
    }); 
    // ============================= For checkout Pages ===================================
});