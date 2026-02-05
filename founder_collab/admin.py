from django.contrib import admin
from .models import FounderNeed, CollabRequest

@admin.register(FounderNeed)
class FounderNeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'founder', 'status', 'week_start_date')
    list_filter = ('status',)

@admin.register(CollabRequest)
class CollabRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'need', 'status', 'created_at')
