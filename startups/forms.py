from django import forms
from .models import StartupProfile

class StartupProfileForm(forms.ModelForm):
    class Meta:
        model = StartupProfile
        fields = ['company_name', 'industry', 'website', 'team_size']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'industry': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'team_size': forms.NumberInput(attrs={'class': 'form-control'}),
        }
