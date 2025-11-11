from django import forms
from .models import Packaging

class PackagingForm(forms.ModelForm):
    class Meta:
        model = Packaging
        fields = ['name', 'quantity', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter packaging name'}),
            'quantity': forms.NumberInput(attrs={'min': 0}),
        }
