# Take home project
This is a simple e-commerce application that a customer can use to purchase a book. The payments functionality has been added along with some additional code to help improve the user experience.

## Application overview
This demo is written in Python with the [Flask framework](https://flask.palletsprojects.com/). You'll need to retrieve a set of testmode API keys from the Stripe dashboard (you can create a free test account [here](https://dashboard.stripe.com/register)) to run this locally.

We're using the [Bootstrap](https://getbootstrap.com/docs/4.6/getting-started/introduction/) CSS framework. It's the most popular CSS framework in the world and is pretty easy to get started with — feel free to modify styles/layout if you like. 

To simplify this project, we're also not using any database here, either. Instead `app.py` includes a simple case statement to read the GET params for `item`. 

If you would like to isolate the dependencies for this app, create a virtual environment:

```
python3 -m venv <your_env_name>
source <your_env_name>/bin/activate
```

To get started, clone the repository and run pip3 to install dependencies:

```
git clone https://github.com/marko-stripe/sa-takehome-project-python && cd sa-takehome-project-python
pip3 install -r requirements.txt
```

Before running the application, you'll need to set two environment variables:

```
export STRIPE_PUBLIC_KEY=<your publishable Stripe key>
export STRIPE_SECRET_KEY=<your secret Stripe key>
```

Then run the application locally:

```
flask run
```

Navigate to [http://localhost:5000](http://localhost:5000) to view the index page.

Once you're done working, you can exit the virtual environment by typing `deactivate`.
