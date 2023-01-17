from django.contrib import admin

from filechecker.models import File, Logs


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('owner', 'file', 'created_at', 'is_checked')
    list_filter = ('is_checked',)


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('file', 'created_at', 'text')