import os
import stripe

from flask import Flask, request, render_template

# Used for printing output in color and with some formatting options
class color:
  PURPLE = '\033[95m'
  CYAN = '\033[96m'
  DARKCYAN = '\033[36m'
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
  END = '\033[0m'

STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
stripe.api_key = STRIPE_SECRET_KEY

# NOTE: The publishable and secret keys are read through environment variables
# In the event that they were not specified, the application will exit and
# some warning output will be printed to notify the user/system running the app
if not STRIPE_PUBLIC_KEY or not STRIPE_SECRET_KEY:
  print(color.BOLD + color.YELLOW + '\n[!] Error: no Stripe keys specified. Please specify your keys using the following commands:' + color.END)
  print(color.BOLD + color.YELLOW + '\texport STRIPE_PUBLIC_KEY=<stripe publishable key>' + color.END)
  print(color.BOLD + color.YELLOW + '\texport STRIPE_SECRET_KEY=<stripe secret key>' + color.END)
  exit(1)

# -----------------------------------------------

app = Flask(__name__,
  static_url_path='',
  template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "views"),
  static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "public"))

# Home route
@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

# Checkout route
@app.route('/checkout', methods=['GET'])
def checkout():
  # Retrieve the item number from the "item" URL parameter
  item = request.args.get('item')
  title = None
  amount = None
  error = None
  client_secret = None

  if item == '1':
    title = 'The Art of Doing Science and Engineering'
    amount = 2300
  elif item == '2':
    title = 'The Making of Prince of Persia: Journals 1985-1993'
    amount = 2500
  elif item == '3':
    title = 'Working in Public: The Making and Maintenance of Open Source'
    amount = 2800
  else:
    # An invalid item ID was provided and the item was not found
    error = 'Item not found!'

  # If the amount was specified, that means the user specified a valid product
  if amount:
    # Create a PaymentIntent based on the amount for this product
    intent = stripe.PaymentIntent.create(
      amount=amount,
      currency='usd',
    )
    # Get the client secret from the newly created PaymentIntent
    client_secret = intent.get('client_secret')

  # Render the "checkout" template
  return render_template('checkout.html',
    public_key=STRIPE_PUBLIC_KEY,
    title=title,
    amount=amount,
    error=error,
    client_secret=client_secret,
  )

# Success route
@app.route('/success', methods=['GET'])
def success():
  error = None
  # Make it an empty dict for now in case the provided ID doesn't match any
  # of our PaymentIntent objects
  payment_intent = {}

  # Attempt to retrieve the PaymentIntent ID from the URL parameters
  pi_id_arg = request.args.get('pi')

  # Check to make sure the user provided this parameter
  if pi_id_arg:
    try:
      # Attempt to retrieve this PaymentIntent
      payment_intent = stripe.PaymentIntent.retrieve(pi_id_arg)
    except stripe.error.InvalidRequestError as err:
      # PaymentIntent was most likely not found if we hit this error case
      error = str(err)
  else:
    # If not, notify them of the error
    error = 'No PaymentIntent ID provided'

  # If payment_intent was never populated with actual data, these "gets" will
  # safely return None
  payment_intent_id = payment_intent.get('id')
  amount = payment_intent.get('amount_received')

  # Render the "success" template
  return render_template('success.html',
    error=error,
    amount=amount,
    payment_intent_id=payment_intent_id
  )


if __name__ == '__main__':
  app.run(port=5000, host='0.0.0.0', debug=True)
