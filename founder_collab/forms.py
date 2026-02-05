from django import forms
from .models import FounderNeed, CollabRequest

class FounderNeedForm(forms.ModelForm):
    class Meta:
        model = FounderNeed
        fields = ['title', 'description', 'category', 'week_start_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-600 focus:border-transparent transition'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-600 focus:border-transparent transition', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-600 focus:border-transparent transition appearance-none'}),
            'week_start_date': forms.DateInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-600 focus:border-transparent transition', 'type': 'date'}),
        }

class CollabRequestForm(forms.ModelForm):
    class Meta:
        model = CollabRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-600 focus:border-transparent transition', 'rows': 2, 'placeholder': 'Introduce yourself...'}),
        }
