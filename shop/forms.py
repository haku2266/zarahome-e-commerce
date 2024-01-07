from django import forms
from .models import ProductVariations


class ColorModelAdminForms(forms.ModelForm):
    code = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))

    class Meta:
        model = ProductVariations
        fields = '__all__'
