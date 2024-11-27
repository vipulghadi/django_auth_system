from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from users.models import User
from django.utils.crypto import get_random_string

def generate_username():
    while True:
        username = get_random_string(length=8)
        if not User.objects.filter(username=username).exists():
            return username
        
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.username:
            user.username = generate_username()
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user
    


class CustomeLoginForm(forms.Form):  
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No account is associated with this email.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        if not email:
            raise forms.ValidationError("Email is required.")
        if not password:
            raise forms.ValidationError("Password is required.")
        
        return cleaned_data

class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Old Password', 'class': 'form-control'}),
        label="Old Password",
        required=True
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password', 'class': 'form-control'}),
        label="New Password",
        required=True
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password', 'class': 'form-control'}),
        label="Confirm New Password",
        required=True
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not self.user.check_password(old_password): 
            raise forms.ValidationError("The old password you entered is incorrect.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        if new_password != confirm_new_password:  # Check if the new passwords match
            raise forms.ValidationError("The new passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        new_password = self.cleaned_data["new_password"]
        if commit:
            self.user.set_password(new_password)  # Set the new password for the user
            self.user.save()
        return self.user

from django import forms

class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(label="Email Address", max_length=254, required=True, widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Enter your registered email address"
    }))
    
    def clean(self):
        cleaned_data = super().clean()
        email= cleaned_data.get("email")

        if not email:  
            raise forms.ValidationError("Invalid email address")
        return cleaned_data
        



    


