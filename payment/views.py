from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.views import APIView
from django.conf import settings
import razorpay
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
import uuid

from .models import Subscription, SubscriptionPlan, Payment
from .serializer import SubscriptionPlanSerializer, PaymentSerializer, SubscriptionSerializer
from .client import RazorpayClient
from account.api.permissions import IsCompanyUser, IsAdminUser




class SubscriptionPlanListView(generics.ListAPIView):
    """"
    API view to list all subscription plans.
    """
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    



class CreateSubscriptionView(APIView):
    
    """"
    API view to create a new subscription for a user.
    """
    
    permission_classes = [IsAuthenticated, IsCompanyUser]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        plan_id = request.data.get('plan_id')

        # validate uuid format
        try:
            uuid.UUID(plan_id)
        except ValueError:
            return Response({"error":"Invalid UUID format"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the subsctription plan
        try:
            plan = SubscriptionPlan.objects.get(uuid=plan_id)
        except SubscriptionPlan.DoesNotExist:
            return Response({"error":"Invalid plan_id"}, status=status.HTTP_400_BAD_REQUEST)

        """
        check if an active subscription already exists for the user
        
        """
        existing_subscription = Subscription.objects.filter(user=request.user.company_profile, plan=plan, is_active=True).first()
        if existing_subscription:
            return Response({"error": "An active subscription already exists for this plan"}, status=status.HTTP_400_BAD_REQUEST)

        #Create subscription
        subscription = Subscription(user=request.user.company_profile, plan=plan)
        subscription.save()

        # serialize the subsription data
        serializer = SubscriptionSerializer(subscription)
        return Response({"message":"Subscription created Successfully", "data":serializer.data}, status=status.HTTP_201_CREATED)

class CreatePaymentView(APIView):

    """
    API view to create a new payment for a subscription.

    Methods:
        - POST: Creates a new payment for the specified subscription.
    """
     
    permission_classes = [IsAuthenticated,IsCompanyUser]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        subscription_id = request.data.get('subscription_id')

        try:
            subscription = Subscription.objects.get(uuid=subscription_id)
        except Subscription.DoesNotExist:
            return Response({"error":"subscription not found"}, status=status.HTTP_404_NOT_FOUND)

        """check if there is already an existing 
        payment for the subscription
        """
        if Payment.objects.filter(subscription=subscription).exists():
            return Response({"error":"Payment already exists for this subscription"}, status=status.HTTP_400_BAD_REQUEST)
        
        amount = int(subscription.plan.price * 100)

        razorpay_client = RazorpayClient()
        order_data = razorpay_client.create_order(amount, "INR")

        # extracting data form razorpay response
        order_id = f"order_{subscription_id}"

        # create payment object
        payment = Payment.objects.create(
            subscription=subscription,
            payment_id=order_id,
            order_id=order_id,
            amount=amount,
            status="pending",
            payment_method="credit card"  # Save the payment method
        )
        serializer = PaymentSerializer(payment)
        return Response({"data":serializer.data, "message": "Payment created successfully"}, status=status.HTTP_201_CREATED)


class VerifyPaymentView(APIView):

    """
    API view to verify a payment made for a subscription.

    Methods:
        - POST: Verifies the payment using the provided Razorpay details.
    """
    
    permission_classes = [IsAuthenticated, IsCompanyUser]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        subscription_id = request.data.get('subscription_id')

        razorpay_client = RazorpayClient()

        # verified = razorpay_client.verify_payment(razorpay_order_id, razorpay_payment_id, subscription_id)
        verified = True

        if verified:
            try:
                payment = Payment.objects.get(order_id=razorpay_order_id, subscription__uuid=subscription_id)
                payment.status="success"
                payment.save()
                return Response({"message": "Payment verified successfully"}, status=status.HTTP_200_OK)
            except Payment.DoesNotExist:
                return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"Payment verificarion failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
admin featues in payment
"""

# class AdminSubscriptionPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
#     """
#     API view to retrieve, update, or delete a subscription plan for admin.
#     """
#     queryset = SubscriptionPlan.objects.all()
#     serializer_class = SubscriptionPlanSerializer
#     permission_classes = [IsAuthenticated, IsAdminUser]
#     authentication_classes = [JWTAuthentication]

class AdminSubscriptionListView(generics.ListAPIView):
    """
    API view to list all subscriptions for admin.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication]

class AdminPaymentListView(generics.ListAPIView):
    """
    API view to list all payments for admin.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication]

