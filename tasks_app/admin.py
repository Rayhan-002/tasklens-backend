from django.contrib import admin
from .models import Tag, Task


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color')
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'priority', 'due_date', 'owner')
    list_filter = ('status', 'priority', 'due_date')
    search_fields = ('title',)
    filter_horizontal = ('tags',)
