from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"placeholder": "Full name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email address"}))
    country = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Country"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Password (min 8 chars)"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"placeholder": "Repeat password"}))

    class Meta:
        model = User
        fields = ("email", "name", "country", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email address"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
