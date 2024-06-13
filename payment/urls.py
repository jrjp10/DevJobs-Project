from django.urls import path
from .views import (CreateSubscriptionView, SubscriptionPlanListView,
                    CreatePaymentView, VerifyPaymentView,
                    AdminSubscriptionListView, AdminPaymentListView, )


urlpatterns = [
    path("company/subscription/plans/", SubscriptionPlanListView.as_view(), name="subscription_list"),
    path("company/subscribe/", CreateSubscriptionView.as_view(), name="subscribe"),
    path("company/subscription/create/", CreatePaymentView.as_view(), name="create_payment"),
    path("company/subscription/verify/", VerifyPaymentView.as_view(), name="verify_payment"),

    # admin
    # path('company/subscription/plans/<uuid:uuid>/', AdminSubscriptionPlanDetailView.as_view(), name='company-subscription-plan-detail'),
    path('company/subscriptions/', AdminSubscriptionListView.as_view(), name='company-subscription-list'),
    path('company/payments/', AdminPaymentListView.as_view(), name='company-payment-list'),
]
