from django.contrib import admin
from .models import *

class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'content',
        'group'
    )

admin.site.register(Answer, AnswerAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'content'
    )

admin.site.register(Question, QuestionAdmin)

class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'key',
        'name'
    )

admin.site.register(Group, GroupAdmin)

class TestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )

admin.site.register(Test, TestAdmin)
