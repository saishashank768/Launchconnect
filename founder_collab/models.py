from django.db import models
from django.conf import settings

class FounderNeed(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('MATCHED', 'Matched'),
        ('CLOSED', 'Closed'),
    )
    founder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='needs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    week_start_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class CollabRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('DECLINED', 'Declined'),
    )
    need = models.ForeignKey(FounderNeed, on_delete=models.CASCADE, related_name='requests')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_collab_requests')
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Request from {self.sender.username} for {self.need.title}"
