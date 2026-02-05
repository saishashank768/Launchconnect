from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'startup', 'status', 'created_at')
    list_filter = ('status', 'job_type')
    search_fields = ('title', 'startup__company_name')
