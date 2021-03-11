const stripe = Stripe('pk_test_51IOunvGzPwyFf2pEno5UaGhJZ3xO8k2OLvFOhiokTJZqq4gHpgFrvxoe88awDIgSKxawKrdOO7maKmiqx4CB22VV00e5RZ6uVY');
const elem = document.getElementById('submit');
const client_secret = elem.getAttribute('data-secret');

const elements = stripe.elements();
const style = {
base: {
  color: "#000",
  lineHeight: '2.4',
  fontSize: '16px'
}
};


const card = elements.create("card", { style: style });
card.mount("#card-element");

card.on('change', function(event) {
  var displayError = document.getElementById('card-errors')
  if (event.error) {
    displayError.textContent = event.error.message;
    $('#card-errors').addClass('alert alert-info');
  } else {
    displayError.textContent = '';
    $('#card-errors').removeClass('alert alert-info');
  }
});



var form = document.getElementById('payment-form');

form.addEventListener('submit', function(e) {
    e.preventDefault();
    const country = $("#country option:selected").val();

    const first_name = document.getElementById("first_name").value;
    const last_name = document.getElementById("last_name").value;
    const email = document.getElementById('email').value;
    const phone_array = new Array();
    count = document.getElementsByName("phone_number").length;
    for (let i = 0; i < count; i++) {
      phone_array.push(document.getElementsByName("phone_number")[i].value);
    }
    phone_number = phone_array.join("-");

    const address = document.getElementById("address").value;
    const city = document.getElementById("city").value;
    const zip_code = document.getElementById("zio_code").value;
    const state_province_region = document.getElementById("state_province_region").value;
    


    // $.ajax({
    //           type: "POST",
    //           url: 'http://localhost:8000/order/add/',
    //           data: {
    //             order_key: client_secret,
    //             first_name,
    //             last_name,
    //             phone_number,
    //             address,
    //             city,
    //             zip_code,
    //             state_province_region,
    //             csrfmiddlewaretoken: CSRF_TOKEN,
    //           },
    //           success: function (json) {
    //             window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
    //           },
    //           error: function (xhr, errmsg, err) {
    //             alert(errmsg);
    //           },
    //         });


    stripe.confirmCardPayment(client_secret, {
      payment_method: {
        card: card,
        billing_details: {
          address:{
              city: city,
              // country: country,
              postal_code: zip_code,
              line1: address,
              line2: state_province_region,
          },
          email : email,
          name: first_name + last_name,
          phone: phone_number,
        },
      }
    }).then(function(result) {
      if (result.error) {
        console.log('payment error')
        console.log(result.error.message);
      } else {
        if (result.paymentIntent.status === 'succeeded') {
          $.ajax({
            type: "POST",
            url: 'http://localhost:8000/order/add/',
            data: {
              order_key: client_secret,
              first_name,
              last_name,
              phone_number,
              address,
              city,
              zip_code,
              state_province_region,
              csrfmiddlewaretoken: CSRF_TOKEN,
            },
            success: function (json) {
              window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
            },
            error: function (xhr, errmsg, err) {
              alert(errmsg);
            },
          });
        }
      }
    });
});