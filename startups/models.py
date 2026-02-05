from django.db import models
from django.conf import settings

class StartupProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='startup_profile')
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    team_size = models.IntegerField(default=1)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.company_name
