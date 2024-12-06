# users/forms.py

from django import forms
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')

    def clean_password2(self):
        # Get the cleaned data for both password fields
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        # Check if the passwords match
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Set the password after hashing
        if commit:
            user.save()  # Save the user to the database
        return user


from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=100, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")