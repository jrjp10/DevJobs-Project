from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from ..models import Job

@receiver(post_save, sender=Job)
def delete_expired_job(sender, instance, **kwargs):
    # Check if the job's last data has passed
    if instance.last_date < timezone.now():
        instance.delete()
