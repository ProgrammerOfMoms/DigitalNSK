from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'firstName',
        'lastName', 
        'phoneNumber',
        'email',
        'role',
    )

admin.site.register(User, UserAdmin)

class ProgressAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'progress',
    )
admin.site.register(Progress, ProgressAdmin)

class EventPointsAdmin(admin.ModelAdmin):
    list_display = (
        'id'
    )
admin.site.register(EventPoints, EventPointsAdmin)

class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'eduInstitution',
        'level',
        'vkURL'
    )

admin.site.register(Participant, ParticipantAdmin)
