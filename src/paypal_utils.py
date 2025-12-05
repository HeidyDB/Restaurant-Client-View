import requests
from base64 import b64encode

# Pon aquí tus credenciales de PayPal
PAYPAL_CLIENT_ID = "TU_CLIENT_ID"
PAYPAL_SECRET = "TU_SECRET"

# Sandbox (pruebas). Para producción cambia a: https://api.paypal.com
PAYPAL_BASE = "https://api.sandbox.paypal.com"


def get_paypal_token():
    """Obtiene un Access Token válido de PayPal."""
    auth_string = f"{PAYPAL_CLIENT_ID}:{PAYPAL_SECRET}"
    encoded_auth = b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(
        f"{PAYPAL_BASE}/v1/oauth2/token",
        data="grant_type=client_credentials",
        headers=headers
    )

    response.raise_for_status()
    return response.json()["access_token"]



def create_paypal_order(total_amount):
    """Crea una nueva orden de pago."""
    token = get_paypal_token()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": str(total_amount)
                }
            }
        ],
        "application_context": {
            "return_url": "http://localhost:3000/paypal-success",
            "cancel_url": "http://localhost:3000/paypal-cancel"
        }
    }

    response = requests.post(
        f"{PAYPAL_BASE}/v2/checkout/orders",
        json=data,
        headers=headers
    )

    response.raise_for_status()
    return response.json()



def capture_paypal_order(order_id):
    """Captura un pago ya aprobado por el usuario."""
    token = get_paypal_token()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(
        f"{PAYPAL_BASE}/v2/checkout/orders/{order_id}/capture",
        headers=headers
    )

    response.raise_for_status()
    return response.json()