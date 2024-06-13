from django.db import models
from django.utils import timezone
from datetime import timedelta
import uuid

from account.models import CompanyProfile


# Create your models here.

class SubscriptionPlan(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('advance', 'Advance'),
    ]
    DURATION_CHOICES = [
        ('30', 'Monthly'),
        ('365', 'Yearly'),
    ]

    name = models.CharField(max_length=50)
    description = models.TextField()
    plan_type = models.CharField(max_length=10, choices=PLAN_CHOICES)
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    job_post_limit = models.IntegerField(default=0, help_text="Use 0 for unlimited job posts")

    def __str__(self):
        return f"{self.name} ({self.plan_type}, {self.duration})"



    
class Subscription(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    """
        Overrides the save method to set the end_date based on the plan's duration if not already set.
    """
    
    def save(self, *args, **kwargs):
        if not self.end_date:
            duration_days = int(self.plan.duration)
            self.end_date = timezone.now() + timedelta(days=duration_days)
        super().save(*args, **kwargs)

    def is_active_subscription(self):
        return self.is_active and self.end_date >= timezone.now()

    def __str__(self):
        return f"{self.user} - {self.plan.name}"



class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('Success', 'Success'),
        ('failed', 'Failed'),
    ]
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, verbose_name="Payment ID")
    order_id = models.CharField(max_length=100, verbose_name="Order ID")
    signature = models.CharField(max_length=200, verbose_name="Signature", null=True, blank=True)
    amount = models.IntegerField(verbose_name="Amount")
    status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default="pending")
    dateTime = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.payment_id)
