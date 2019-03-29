from django.contrib import admin
from .models import *

class EventStageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name"
    )

admin.site.register(EventStage, EventStageAdmin)

class CompetenceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name"
    )

admin.site.register(Competence, CompetenceAdmin)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "img",
        "date",
        "time",
        "duration",
        "venue",
        "format_event",
        "format_task",
        "max_partiсipants",
        "partiсipants",
        "count",
        "partner",
        "manager_name",
        "manager_position",
        "phonenumber"
    )

admin.site.register(Event, EventAdmin)
