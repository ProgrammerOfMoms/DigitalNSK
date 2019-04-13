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
        "name",
        "level",
        "parent"
    )

admin.site.register(Competence, CompetenceAdmin)

class PointAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "competence",
        "value"
    )

admin.site.register(Point, PointAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "img",
        "date",
        "time",
        "venue",
        "format_event",
        "max_partiсipants",
        "partiсipants",
        "partner",
        "manager_name",
        "manager_position",
        "phonenumber"
    )

admin.site.register(Event, EventAdmin)
