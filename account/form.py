from django import forms
from .models import Destination


class UserFrom(forms.ModelForm):
    class Meta:
        model = Destination
        widgets = {
            'password1': forms.PasswordInput(),
        }
        fields = ['username', 'password1', 'password2', 'mobile', 'dob']


class LoginForm(forms.ModelForm):
    class Meta:
        model = Destination
        widgets = {
            'password1': forms.PasswordInput(),
        }
        fields = ['username', 'password1']





