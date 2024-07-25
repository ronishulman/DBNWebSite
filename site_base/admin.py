# admin.py
from django.contrib import admin
from .models import WorkSchedule
from .models import UpdateMessages

admin.site.register(WorkSchedule)
admin.site.register(UpdateMessages)