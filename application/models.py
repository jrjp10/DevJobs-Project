from django.db import models
from django.conf import settings
import uuid

from job.models import Job
from account.models import CandidateProfile


# Create your models here.

class Application(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('Declined', 'Declined'),
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
    ], default='Pending')

    def __str__(self) -> str:
        return f"{self.candidate} applied for {self.job}"