from django.contrib import admin
from .models import *


class NewsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'html_code',
        'photo',
        'date'
    )

admin.site.register(News, NewsAdmin)
