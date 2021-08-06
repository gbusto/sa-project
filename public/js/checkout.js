var stripe = Stripe(publicKey);

var form = $("#payment-form");

var emailInput = $("#email");

var cardIsComplete = false;

function showCardError(message) {
  var errorDiv = $("#card-errors");
  errorDiv.append('<p class="text-danger">' + message + '</p>');
}

function clearCardError(message) {
  var errorDiv = $("#card-errors");
  errorDiv.empty();
}

function disableButton() {
  $("#pay-button").prop("disabled", true);
}

function enableButton() {
  $("#pay-button").prop("disabled", false);
}

function resetPayButton() {
  var button = $("#pay-button");
  button.html("Retry payment");
  button.prop("disabled", false);
}

function isEmailValid() {
  var re = /\w+[@]\w+\.\w{2}/;
  var text = $("#email").val();
  return re.exec(text);
}

emailInput.on("input", function(e) {
  updateAllowPayment();
});

form.on("submit", function(e) {
  clearCardError();

  if (!inputIsComplete()) {
    return;
  }
  var payButton = $("#pay-button");
  var email = $("#email").val();
  e.preventDefault();
  disableButton();
  payButton.html('<div class="spinner-border text-light mr-2"><span class="sr-only">Loading...</span></div>Processing Payment...');

  stripe.confirmCardPayment(clientSecret, {
    payment_method: {
      card: card,
      billing_details: {
        email: email
      }
    }
  }).then(function(result) {
    if (result.error) {
      showCardError(result.error.message);
      resetPayButton();
    } else {
      // The payment has been processed!
      if (result.paymentIntent.status === 'succeeded') {
        window.location.href = "/success?pi=" + result.paymentIntent.id;
      }
    }
  });
});

var elements = stripe.elements({
  locale: "auto"
});

/**
 * Card Element
 */
var card = elements.create("card", {
  style: {
    base: {
      color: "#32325D",
      fontWeight: 500,
      fontFamily: "Inter, Open Sans, Segoe UI, sans-serif",
      fontSize: "16px",
      fontSmoothing: "antialiased",

      "::placeholder": {
        color: "#CFD7DF"
      }
    },
    invalid: {
      color: "#E25950"
    }
  }
});

card.on("change", ({complete, error}) => {
  let displayError = document.getElementById("card-errors");
  if (error) {
    displayError.textContent = error.message;
  } else {
    displayError.textContent = "";
  }

  if (complete) {
    cardIsComplete = true;
  }
  else {
    cardIsComplete = false;
  }

  updateAllowPayment();
});

function inputIsComplete() {
  return cardIsComplete && emailInput.val().length > 0 && isEmailValid();
}

function updateAllowPayment() {
  if (inputIsComplete()) {
    enableButton();
  }
  else {
    disableButton();
  }
}

card.mount("#stripe-elements");
