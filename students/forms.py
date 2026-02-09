from django import forms
from .models import StudentProfile

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'current_status', 'education', 'experience_level', 'skills', 'preferred_roles', 
            'availability', 'weekly_hours', 'start_date', 'work_mode',
            'resume_url', 'portfolio_url', 'actively_looking'
        ]
        widgets = {
            'current_status': forms.Select(attrs={'class': 'form-select', 'id': 'id_current_status'}),
            'education': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'University, Degree (Optional)'}),
            'experience_level': forms.Select(attrs={'class': 'form-select', 'id': 'id_experience_level'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Python, React, Figma, Sales, Cooking...'}),
            'preferred_roles': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Backend, Product Manager, Chef, Designer...'}),
            'availability': forms.Select(attrs={'class': 'form-select'}),
            'weekly_hours': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 168}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'work_mode': forms.Select(attrs={'class': 'form-select'}),
            'resume_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link to Resume / LinkedIn'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link to Portfolio / GitHub / Social'}),
            'actively_looking': forms.CheckboxInput(attrs={'class': 'form-check-input peer', 'style': 'width:1.25rem;height:1.25rem;'}),
        }
