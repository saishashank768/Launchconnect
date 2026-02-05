from django.db import models
from django.conf import settings

class StartupProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='startup_profile')
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    team_size = models.IntegerField(default=1)
    is_verified = models.BooleanField(default=False)
    
    @property
    def hire_score(self):
        """Calculate reputation based on successful conversions (Phase 6)"""
        from applications.models import Application
        conversions = Application.objects.filter(job__startup=self, is_conversion=True).count()
        if conversions == 0: return 0
        # Simple algorithm: 10 points per conversion, capped at 100
        return min(conversions * 10, 100)
    
    def __str__(self):
        return self.company_name
