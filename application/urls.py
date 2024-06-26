from django.urls import path, include
from .views import *


urlpatterns = [
    path('application/apply/', ApplicationCreateAPIView.as_view(), name='candidate_application'),
    path('application/list/', ApplicationsListAPIView.as_view(), name='application total'),
    path('application/<uuid:uuid>/status/', ApplicationUpdateAPIView.as_view(), name='application_company_update'),
    path('company/download/resumes/', DownloadResumeAPIView.as_view(), name='download_resumes'),
    
]
