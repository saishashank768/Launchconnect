from django.db import models
from django.conf import settings

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    resume_url = models.URLField(blank=True, null=True)
    skills = models.TextField(help_text="Comma-separated list of skills")
    education = models.CharField(max_length=255, blank=True, help_text="University/Degree (Optional for non-students)")
    availability = models.CharField(max_length=50, choices=[
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('flexible', 'Flexible'),
    ], default='full_time')
    
    # Universal Talent Fields
    current_status = models.CharField(
        max_length=50,
        choices=[
            ('student', 'Student'),
            ('fresher', 'Fresher / Unemployed'),
            ('switcher', 'Career Switcher'),
            ('skilled', 'Skilled Worker (Non-degree)'),
        ],
        default='student',
        help_text="Current professional status"
    )
    
    # Normalized Experience Field
    experience_level = models.CharField(
        max_length=20,
        choices=[
            # Student Levels
            ('student_1', '1st Year'),
            ('student_2', '2nd Year'),
            ('student_3', '3rd Year'),
            ('student_final', 'Final Year'),
            # Professional Levels
            ('entry', 'Entry Level (<1 year)'),
            ('mid', 'Mid Level (1-3 years)'),
            ('senior', 'Senior (3-5 years)'),
            ('expert', 'Expert (5+ years)'),
        ],
        default='student_1',
        help_text="Academic year or professional experience level"
    )
    
    portfolio_url = models.URLField(blank=True, null=True, help_text="Portfolio / Github / Social Link")

    preferred_roles = models.CharField(
        max_length=255,
        help_text="Target roles (e.g. Backend Engineer, Product Designer)",
        default="",
        blank=True
    )
    weekly_hours = models.PositiveIntegerField(
        help_text="Hours available per week",
        default=20
    )
    start_date = models.DateField(
        null=True, blank=True,
        help_text="Earliest available start date"
    )
    work_mode = models.CharField(
        max_length=20,
        choices=[
            ('remote', 'Remote'),
            ('onsite', 'On-site'),
            ('hybrid', 'Hybrid'),
            ('any', 'Any'),
        ],
        default='any',
        help_text="Work setting preference"
    )
    
    actively_looking = models.BooleanField(default=True, help_text="Whether the student is actively looking for jobs (controls resume push to companies)")
    
    def __str__(self):
        return self.user.username
