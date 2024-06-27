from django.urls import path, include
from .views import *

app_name = 'account'  # namespace for  this app

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user_register'),
    path("activate/<str:uidb64>/<str:token>/", ActivateAccountView.as_view(), name="activate"),
    path('login/', LoginView.as_view(), name='user_login'),

    path("candidate/create/", CandidateProfileCreateView.as_view(),  name='candidate_profile_create'),
    path("candidate/list/", CandidateProfileListView.as_view(), name='candidate_profile_update'),
    path('candidate/<uuid:uuid>/', CandidateProfileCRUDView.as_view(), name='candidate-profile-detail'),
    

    path("company/create/", CompanyProfileCreateView.as_view(),  name='company_profile_create'),
    path("company/list/", CompanyProfileListView.as_view(), name='company_profile_update'),
    path('company/<uuid:uuid>/', CompanyProfileCRUDView.as_view(), name='company-profile-detail'),
    path("public/companies/", CompanyProfilePublicListView.as_view(), name='public_company_view'),


    # urls for Admin Dashboard
    path("users/", UserListView.as_view(),  name='all-users'),
    path('users/<uuid:uuid>/', UserDetailView.as_view(), name='user-detail'),
    path("candidates/", CandidateProfileListView.as_view(),  name='candidates'),
    path("companies/", CompanyProfileListView.as_view(),  name='companies'),
    


]
