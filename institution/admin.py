from django.contrib import admin
from .models import *

class InstitutionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    
admin.site.register(Institution, InstitutionAdmin)