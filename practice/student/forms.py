from django import forms
from accounts.models import CustomUser

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['phone', 'email']
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'Введите номер телефона'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Введите email'}),
        }