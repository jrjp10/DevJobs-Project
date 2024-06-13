from rest_framework.serializers import ValidationError
from rest_framework import status
from django.conf import settings
import razorpay


# Initialize the Razorpay client
client = razorpay.Client(auth=(
    settings.RAZORPAY_KEY_ID,
    settings.RAZORPAY_KEY_SECRET
))

class RazorpayClient:

    """
    A client class to interact with the Razorpay API for creating orders and verifying payments.
    """
    
    def create_order(self, amount, currency):
        data = {
            "amount": amount,   # Amount should be in paise
            "currency": currency
        }
        try:
            order_data = client.order.create(data=data)
            return order_data
        except Exception as e:
            raise ValidationError(
                {
                    "status_code" : status.HTTP_400_BAD_REQUEST,
                    "message" : str(e),
                }
            )
        
    def verify_payment(self, razorpay_order_id,razorpay_payment_id, razorpay_signature):
        try:   
            return client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
        except Exception as e:
            raise ValidationError(
                {
                   "status_code":status.HTTP_400_BAD_REQUEST,
                   "message": str(e)
                }
            )