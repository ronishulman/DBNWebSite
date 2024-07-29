from django.core.management.base import BaseCommand
from django.utils import timezone
from site_base.models import UpdateMessages 

class Command(BaseCommand):
    help = 'Clear old update messages that are older than a week.'

    def handle(self, *args, **options):
        one_week_ago = timezone.now() - timezone.timedelta(weeks=1)

        print(f"Clearing messages older than: {one_week_ago}")


        count_before = UpdateMessages.objects.filter(created_at__lt=one_week_ago).count()
        print(f"Messages to delete: {count_before}")

        deleted_count, _ = UpdateMessages.objects.filter(created_at__lt=one_week_ago).delete()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted_count} old update messages.'))