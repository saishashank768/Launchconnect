from django import forms
from .models import StudentProfile

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['education', 'skills', 'availability', 'resume_url']
        widgets = {
            'education': forms.TextInput(attrs={'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'availability': forms.Select(attrs={'class': 'form-select'}),
            'resume_url': forms.URLInput(attrs={'class': 'form-control'}),
        }
