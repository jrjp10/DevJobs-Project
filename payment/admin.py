from django.contrib import admin
from .models import Payment, SubscriptionPlan, Subscription


# Register your models here.
admin.site.register(Payment)
admin.site.register(SubscriptionPlan)
admin.site.register(Subscription)

