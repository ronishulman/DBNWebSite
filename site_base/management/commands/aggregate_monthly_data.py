from django.core.management.base import BaseCommand
from site_base.views import aggregate_monthly_data
from django.http import HttpRequest
from django.utils import timezone 

class Command(BaseCommand):
    help = 'Run aggregate monthly data process'

    def handle(self, *args, **options):

        today = timezone.now().date()
        
        print(f"Aggregate Monthly Data command triggered on {today}.")

        if today.day == 1:
            aggregate_monthly_data()
            self.stdout.write(self.style.SUCCESS('Aggregate monthly data command executed.'))