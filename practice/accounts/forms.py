from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Логин"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Пароль"}
        )
    )
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser

        fields = [
            "last_name",
            "first_name",
            "middle_name",
            "phone",
            "email",
        ]