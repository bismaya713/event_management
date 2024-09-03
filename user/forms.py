from django import forms
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm,SetPasswordForm
from user.models import User
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re
# def validate_contact(value):
#     if not value.isdigit() or len(value) != 10:
#         raise ValidationError('Contact number must be exactly 10 digits.')

class SignUpForm(forms.Form):

    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter your full Name'}))
    email = forms.EmailField(max_length=254,
                             widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Enter valid email address'}))
    contact = forms.CharField(max_length=10,
        validators=[RegexValidator(regex='^[9876]\d{9}$')],widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Mobile Number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter Confirm Password'}))



    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email address already exists")
        return email

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if User.objects.filter(contact=contact).exists():
            raise forms.ValidationError("Contact number already exists")
        return contact


    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6 :
            raise ValidationError('Password length must be 6 characters.')

        if not re.search(r'[A-Za-z]', password):
            raise ValidationError('Password must contain at least one alphabet.')

        if not re.search(r'[0-9]', password):
            raise ValidationError('Password must contain at least one number.')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Password must contain at least one special character.')

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

        return cleaned_data

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter valid email address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter password'}))
    
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user found with this email address.")
        return email
 
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
