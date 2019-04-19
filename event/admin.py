from django.contrib import admin
from .models import *

class SideCompetenceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name"
    )

admin.site.register(SideCompetence, SideCompetenceAdmin)

class SideCompetenceAddAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )

admin.site.register(SideCompetenceAdd, SideCompetenceAddAdmin)

class MainCompetenceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name"
    )

admin.site.register(MainCompetence, MainCompetenceAdmin)

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
        "value"
    )

admin.site.register(Point, PointAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
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
