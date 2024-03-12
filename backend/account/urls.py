from django.urls  import path, include
from .import views
from account.views import UserRegistrationView, LoginView
# CompanyProfileAPIView,CandidateProfileAPIView, UserChangePasswordUpdateView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('login/', LoginView.as_view(), name= 'login'),
    # path('companyprofile/', CompanyProfileAPIView.as_view(), name='companyprofile'),
    # path('candidateprofile/', CandidateProfileAPIView.as_view(), name='candidateprofile'),
    # path('change-password/',UserChangePasswordUpdateView.as_view(),name="change-password"),
]