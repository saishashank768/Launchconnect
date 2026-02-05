from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('startup', 'Startup'),
        ('founder', 'Founder'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    def is_student(self):
        return self.role == 'student'
        
    def is_startup(self):
        return self.role == 'startup'
        
    def is_founder(self):
        return self.role == 'founder'
        
    def is_admin_role(self):
        return self.role == 'admin'
