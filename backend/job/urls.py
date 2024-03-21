from django.urls import path
from .views import JobListCreate, JobRetrieveUpdateDestroy, AllJob, GetTopicStats

urlpatterns = [
    path('all-jobs/', AllJob.as_view(), name='all-jobs'), # for getting all jobs in the database
    path('jobs/new/', JobListCreate.as_view(), name= 'job-list-create'),
    path('jobs/<int:pk>/', JobRetrieveUpdateDestroy.as_view(), name='job-retrieve-update-destroy'),
    path('topic-stats/<str:topic>/',GetTopicStats.as_view(), name='topic-stats'),

]