from django import forms
from .models import FounderNeed, CollabRequest

class FounderNeedForm(forms.ModelForm):
    class Meta:
        model = FounderNeed
        fields = ['title', 'description', 'week_start_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'week_start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class CollabRequestForm(forms.ModelForm):
    class Meta:
        model = CollabRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Introduce yourself...'}),
        }
