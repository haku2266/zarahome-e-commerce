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
                'hx-trigger': 'keyup changed delay:500ms',
                'hx-target': '#phone-target',
                'hx-post': "/user/phone-validate/",
            }),
            'password': forms.PasswordInput(
                attrs={
                    'hx-trigger': 'keyup changed delay:500ms',
                    'hx-target': '#password-target',
                    'hx-post': "/user/password-validate/"
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'hx-trigger': 'keyup changed delay:500ms',
                    'hx-target': '#email-target',
                    'hx-post': "/user/email-validate/"
                }
            )
        }

    def clean_confirm_password(self):
        if self.cleaned_data['confirm_password'] != self.cleaned_data['password']:
            raise ValidationError('Passwords do not match')
