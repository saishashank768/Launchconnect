from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('startup', 'Startup'),
        ('founder', 'Founder'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=255, unique=True, blank=True, null=True)
    
    def is_student(self):
        return self.role == 'student'
        
    def is_startup(self):
        return self.role == 'startup'
        
    def is_founder(self):
        return self.role == 'founder'
        
    def is_admin_role(self):
        return self.role == 'admin'

    @property
    def collab_score(self):
        """Founder reputation based on accepted collab requests (Phase 6)"""
        if self.role != 'founder': return 0
        from founder_collab.models import CollabRequest
        accepted = CollabRequest.objects.filter(need__founder=self, status='ACCEPTED').count()
        return min(accepted * 5, 100) # 5 points per collaboration

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"
