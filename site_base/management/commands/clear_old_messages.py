from django.core.management.base import BaseCommand
from django.utils import timezone
from site_base.models import UpdateMessages 

class Command(BaseCommand):
    help = 'Clear old update messages that are older than a week.'

    def handle(self, *args, **options):
        today = timezone.now().date()
        print("im in the handle")
        if today.weekday() == 0: 
            one_week_ago = timezone.now() - timezone.timedelta(weeks=1)
            UpdateMessages.objects.filter(created_at__lt=one_week_ago).delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted last week update messages.'))
