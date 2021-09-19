from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import validate_email

class NewUserForm(UserCreationForm):
    username = forms.CharField(label="Username", min_length=5)
    email = forms.EmailField(label="E-mail", validators=[validate_email])

    def username_clean(self):
        username = self.cleaned_data['username']
        created = User.objects.filter(username=username)
        if created.exists():
            raise ValidationError("Username already exists!")
        return username
    
    def email_clean(self):
        email = self.cleaned_data['email']
        created = User.objects.filter(email=email)
        if created.exists():
            raise ValidationError("Email already exists!")
        return email
    
    def clean_password2(self):
        password = self.cleaned_data['password1']
        confirm_password = self.cleaned_data['password2']
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Password don't match")
        return confirm_password
    
    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password2']
        )
        return user