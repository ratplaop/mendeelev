
from yookassa import Configuration, Payment
import uuid

class PaymentService:
    @staticmethod
    def init_payment(amount, description):
        Configuration.account_id = os.getenv('YOOKASSA_SHOP_ID')
        Configuration.secret_key = os.getenv('YOOKASSA_SECRET_KEY')

        payment = Payment.create({
            "amount": {
                "value": str(amount),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://www.example.com/return_url"
            },
            "capture": True,
            "description": description,
            "metadata": {
                "order_id": str(uuid.uuid4())
            }
        })
        
        return payment.confirmation.confirmation_url
