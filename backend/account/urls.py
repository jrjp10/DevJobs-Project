from django.urls  import path, include
from .import views
from account.views import UserRegistrationView, LoginView, CompanyProfileCreateView, CandidateProfileCreateView, CompanyProfileRetrieveUpdateDestroyView, CandidateProfileRetrieveUpdateDestroyView
# UserChangePasswordUpdateView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('login/', LoginView.as_view(), name= 'login'),
    path('company-profiles/', CompanyProfileCreateView.as_view(), name='company-profile-list'),
    path('company-profiles/<int:pk>/', CompanyProfileRetrieveUpdateDestroyView.as_view(), name='company-profile-detail'),
    path('candidate-profiles/', CandidateProfileCreateView.as_view(), name='candidate-profile-list'),
    path('candidate-profiles/<int:pk>/', CandidateProfileRetrieveUpdateDestroyView.as_view(), name='candidate-profile-detail'),
    # path('companyprofile/', CompanyProfileView.as_view(), name='companyprofile'),
    # path('candidateprofile/', CandidateProfileView.as_view(), name='candidateprofile'),
    # path('change-password/',UserChangePasswordUpdateView.as_view(),name="change-password"),
]