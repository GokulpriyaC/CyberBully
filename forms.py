from django import forms


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


# forms.py
from django import forms

class BlockUserForm(forms.Form):
    instaid = forms.CharField(label="Instagram ID", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Instagram ID to block...'
    }))

