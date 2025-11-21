from django import forms
from .models import Flavor, Ingredient, Topping, Packaging

class PackagingForm(forms.ModelForm):
    class Meta:
        model = Packaging
        fields = ['name', 'price', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter packaging name'}),
            'quantity': forms.NumberInput(attrs={'min': 0}),
        }

# --- Flavor Form ---
class FlavorForm(forms.ModelForm):
    class Meta:
        model = Flavor
        fields = ['name', 'quantity', 'price', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter flavor name',
                'class': 'form-control'
            }),
            'quantity': forms.NumberInput(attrs={
                'min': 0,
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'min': 0,
                'step': '0.01',
                'class': 'form-control'
            }),
        }


# --- Ingredient Form ---
class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter ingredient name',
                'class': 'form-control'
            }),
            'quantity': forms.NumberInput(attrs={
                'min': 0,
                'class': 'form-control'
            }),
            'unit': forms.TextInput(attrs={
                'placeholder': 'e.g., grams, ml, pcs',
                'class': 'form-control'
            }),
        }


# --- Topping Form ---
class ToppingForm(forms.ModelForm):
    class Meta:
        model = Topping
        fields = ['name', 'quantity', 'price', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter topping name',
                'class': 'form-control'
            }),
            'quantity': forms.NumberInput(attrs={
                'min': 0,
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'min': 0,
                'step': '0.01',
                'class': 'form-control'
            }),
        }


