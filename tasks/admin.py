from django.contrib import admin

from .models import *


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
