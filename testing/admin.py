from django.contrib import admin
from .models import *

class TestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )

admin.site.register(Test, TestAdmin)
