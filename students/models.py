from django.db import models
from django.conf import settings

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    resume_url = models.URLField(blank=True, null=True)
    skills = models.TextField(help_text="Comma-separated list of skills")
    education = models.CharField(max_length=255)
    availability = models.CharField(max_length=50, choices=[
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
    ], default='full_time')
    
    def __str__(self):
        return self.user.username
