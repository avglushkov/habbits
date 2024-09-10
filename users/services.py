import requests
import stripe
from config.settings import STRIPE_API_KEY, TELEGRAM_URL, TELEGRAM_TOKEN

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product):
    """Create product"""

    return stripe.Product.create(name=f"{product}")


def create_stripe_price(price, product):
    """Create product price"""

    return stripe.Price.create(
        currency="rub",
        unit_amount=price * 100,
        product=product.get('id')
    )


def create_stripe_session(price):
    """Create payment session"""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')

def send_telegram_message(chat_id,message):

    params = {
        'text': message,
        'chat_id': chat_id,
    }
    requests.get(f'{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMassage', params=params)