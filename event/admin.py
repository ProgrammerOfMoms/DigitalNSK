from django.contrib import admin
from .models import *

class EventAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "image",
        "description",
        "competence",
        "date",
        "time",
        "duration",
        "venue",
        "format_event",
        "format_task",
        "max_partiсipant",
    )

admin.site.register(Event, EventAdmin)
