from django.contrib import admin

from filechecker.models import File, Logs


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('owner', 'file', 'created_at', 'status')
    list_filter = ('status',)


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('file', 'created_at', 'text')