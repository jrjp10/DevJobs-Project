from typing import Any
from django.core.management.base import BaseCommand
from django.utils import timezone
from account.models import User

class Command(BaseCommand):
    help = 'Deletes inacive user account after a certain period of time.'

    def handle(self, *args, **options):
        # Define the threshold time
        threshold_time = timezone.now() - timezone.timedelta(days=1)

        # Retrive inactive users
        inactive_users = User.objects.filter(
            is_active=False, created_at__lte=threshold_time)
        
        # Delete inactive users one by one
        deleted_count = 0
        for user in inactive_users:
            user.delete()
            deleted_count += 1
        
        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_count} inactive user(s)."))