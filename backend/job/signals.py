from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Job

@receiver(post_save, sender=Job)

def delete_expired_job(sender, instance, **kwargs):
    """
    Signal handler to delete expired job posting
    """
    if instance.last_date and instance.last_date < timezone.now():
        instance.delete()