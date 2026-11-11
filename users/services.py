import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_checkout_session(item_name, item_price):
    """
    Создает продукт и сессию. item_name - название, item_price - цена.
    """
    try:
        product = stripe.Product.create(name=item_name)

        price = stripe.Price.create(
            product=product.id,
            unit_amount=int(item_price * 100),
            currency="rub",
        )

        # Убрали payment_method_types, так как Stripe его удалил
        session = stripe.checkout.Session.create(
            line_items=[{
                'price': price.id,
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/success/',
            cancel_url='http://localhost:8000/cancel/',
        )

        return {
            "url": session.url,
            "session_id": session.id
        }
    except Exception as e:
        raise Exception(f"Ошибка Stripe: {str(e)}")

def get_stripe_payment_status(session_id):
    """
    Запрашивает у Stripe актуальный статус сессии.
    Возвращает 'paid', 'unpaid' или None.
    """
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session.payment_status
    except Exception:
        return None