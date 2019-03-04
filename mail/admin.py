from django.contrib import admin
from .models import *

class LinkRecoveryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'link',
    )

admin.site.register(RecoveryLink, LinkRecoveryAdmin)


