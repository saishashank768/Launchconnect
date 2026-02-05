from django.db import models
from startups.models import StartupProfile

class Job(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
        ('HIRED', 'Hired'),
    )
    JOB_TYPE_CHOICES = (
        ('internship', 'Internship'),
        ('job', 'Full-time Job'),
    )
    
    startup = models.ForeignKey(StartupProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='internship')
    stipend = models.CharField(max_length=100, help_text="e.g. $1000/mo or Equity")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} at {self.startup.company_name}"
