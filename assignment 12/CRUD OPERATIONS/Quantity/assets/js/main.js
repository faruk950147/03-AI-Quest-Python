/*-------------------Quantity change--------------------- */
var proQty = $('.pro-qty')
// proQty.prepend('<span class="dec qtybtn">-</span>')
// proQty.append('<span class="inc qtybtn">+</span>')
proQty.on('click', '.qtybtn', function () {
    var $button = $(this)
    var oldValue = $button.parent().find('input').val()
    if ($button.hasClass('inc')) {
        var newVal = parseInt(oldValue) + 1
    } 
    else {
        // Don't allow decrementing below one
        if (oldValue > 1) {
            var newVal = parseInt(oldValue) - 1
        } 
        else {
            newVal = 1
            }
        }
    $button.parent().find('input').val(newVal)
});