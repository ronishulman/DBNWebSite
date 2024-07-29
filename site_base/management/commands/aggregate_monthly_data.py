from django.core.management.base import BaseCommand
from site_base.views import aggregate_monthly_data
from django.http import HttpRequest
from django.utils import timezone 

class Command(BaseCommand):
    help = 'Run aggregate monthly data process'

    def handle(self, *args, **options):

        today = timezone.now().date()
        
        print(f"Aggregate Monthly Data command triggered on {today}.")

        if today.day == 29:

            request = None 
            aggregate_monthly_data(request)
            self.stdout.write(self.style.SUCCESS('Successfully aggregated monthly data.'))
        else:
            self.stdout.write(self.style.WARNING('Today is not the first day of the month. Skipping aggregation.'))