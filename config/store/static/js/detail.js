$(document).on('click', '#cart-add-button', function(e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '{% url "cart:cart_add" %}',
        data: {
            product_id: $('cart-add-button').val(),
            csrfmiddlewaretoken: "{{crsf_token}}",
            action: 'POST'
        },
        success: function(json) {

        },
        error: function(xhr, errmsg, err) {

        }
    })
});