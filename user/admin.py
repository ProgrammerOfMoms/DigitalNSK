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

class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'eduInstitution',
        'level',
        'vkURL'
    )

admin.site.register(Participant, ParticipantAdmin)
