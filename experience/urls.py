from django.urls import path, include
from .views import *


urlpatterns = [
    path('experience/', ExperienceListAPIView.as_view(), name='candidate_experience'),
    path('experience/<uuid:uuid>/', ExperienceDetailsAPIView.as_view(), name='candidate_experience_CRUD'),
    
]