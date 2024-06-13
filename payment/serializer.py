from rest_framework import serializers
from .models import SubscriptionPlan, Subscription, Payment



class SubscriptionPlanSerializer(serializers.ModelSerializer):

    """
    Serializer for the SubscriptionPlan model.

    This serializer converts SubscriptionPlan model instances into JSON format
    and vice versa. It includes all fields of the SubscriptionPlan model.
    """
     
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    # user_name = serializers.CharField(source='user.name', read_only=True)
    # plan_name = serializers.CharField(source='plan.name', read_only=True)
    class Meta:
        model = Subscription
        fields = '__all__'

       
        

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

