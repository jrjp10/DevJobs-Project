from django.db import models
from django.conf import settings
import uuid

from account.models import CandidateProfile

# Create your models here.

class Experience(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='experiences')
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.position} at {self.company_name}"
    
    @property
    def id(self):
        return self.uuid
