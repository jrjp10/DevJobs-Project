from django.urls import path
from .views import CreateJob,JobRetrieveUpdateDestroy ,AllJob

urlpatterns = [
    path('jobs/new/', CreateJob.as_view(), name= 'job-list-create'),
    path('jobs/<uuid:uuid>/', JobRetrieveUpdateDestroy.as_view(), name='job-CRUD'),
    path('jobs/', AllJob.as_view(), name='all-job'),


]
