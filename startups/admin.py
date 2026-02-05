from django.contrib import admin
from .models import StartupProfile

@admin.register(StartupProfile)
class StartupProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'is_verified', 'team_size')
    list_filter = ('is_verified',)
    search_fields = ('company_name',)
    actions = ['verify_startups']
    
    def verify_startups(self, request, queryset):
        queryset.update(is_verified=True)
