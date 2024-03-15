from django.urls  import path, include
from .import views
from account.views import UserRegistrationView, LoginView, CompanyProfileCreateView, ComapanyProfileListView, CandidateProfileCreateView, CandidateProfileListView,CompanyProfileRetrieveUpdateDestroyView, CandidateProfileRetrieveUpdateDestroyView
# UserChangePasswordUpdateView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('login/', LoginView.as_view(), name= 'login'),

    path('create-company-profiles/', CompanyProfileCreateView.as_view(), name='company-profile-list'),
    path('companyprofiles-list/', ComapanyProfileListView.as_view(),name='company-list'),
    path('company-profiles/<int:pk>/', CompanyProfileRetrieveUpdateDestroyView.as_view(), name='company-profile-detail'),
    
    path('create-candidate-profiles/', CandidateProfileCreateView.as_view(), name='candidate-profile-list'),
    path('candidateprofiles-list/', CandidateProfileListView.as_view(),name='candidate-list'),
    path('candidate-profiles/<int:pk>/', CandidateProfileRetrieveUpdateDestroyView.as_view(), name='candidate-profile-detail'),
    
    # path('change-password/',UserChangePasswordUpdateView.as_view(),name="change-password"),
]