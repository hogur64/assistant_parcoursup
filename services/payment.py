import stripe

# ---- ⚠️ TA CLÉ SECRÈTE ICI ⚠️ ----
import os
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# ---- TON PRICE ID ----
PRICE_ID = "price_1SdTut2Olkgt4jVueIJyYoio"


def create_checkout_session(success_url, cancel_url):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": PRICE_ID,
                "quantity": 1,
            }],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session.url

    except Exception as e:
        return f"Erreur Stripe : {e}"
