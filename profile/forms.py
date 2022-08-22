from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class ProfileForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your email'
                                      })
    )
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']
