const stripe = Stripe('pk_test_51IOunvGzPwyFf2pEno5UaGhJZ3xO8k2OLvFOhiokTJZqq4gHpgFrvxoe88awDIgSKxawKrdOO7maKmiqx4CB22VV00e5RZ6uVY');
const elem = document.getElementById('submit');
const clientsecret = elem.getAttribute('data-secret');

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
    // var displayError = document.getElementById('card-errors')
    // if (event.error) {
    //   displayError.textContent = event.error.message;
    //   $('#card-errors').addClass('alert alert-info');
    // } else {
    //   displayError.textContent = '';
    //   $('#card-errors').removeClass('alert alert-info');
    // }
    // });
    
    var form = document.getElementById('payment-form');
    
    form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const name = document.getElementById("custName").value;
    const address = document.getElementById("custAdd").value;
    const phone_number = document.getElementById("custAdd2").value;
    const city = document.getElementById("postCode").value;
    const zip_code = document.getElementById("postCode").value;
    const state_province_region = document.getElementById("postCode").value;
    })
});