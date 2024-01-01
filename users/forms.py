from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'password')
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'hx-trigger': 'keyup',
                'hx-target': '#reg-form',
                'hx-post': "/user/flag-control/",
                'hx-swap': 'outerHTML'
            })
        }

    def clean_confirm_password(self):
        if self.cleaned_data['confirm_password'] != self.cleaned_data['password']:
            raise ValidationError('Passwords do not match')
