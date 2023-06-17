from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}), 
        label="Пароль",
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8 or len(password) > 50:
            raise ValidationError(_('Пароль должен быть длинной не менее 8 и не более 50 символов'))

        lowercase_letters = any(c.islower() for c in password)
        uppercase_letters = any(c.isupper() for c in password)
        numbers = sum(c.isdigit() for c in password)

        if not lowercase_letters or not uppercase_letters or numbers < 4:
            raise ValidationError(_('Пароль должен содержать, как минимум одну букву в верхнем и в нижнем регистрах и от 4 цифр'))

        return password


    class Meta:
        model = User
        fields = ['email', 'name_lastname', 'username', 'password']
        labels = {
            'email': 'Эл. почта',
            'name_lastname': 'Имя и фамилия',
            'username': 'Имя пользователя',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Эл. почта'}),
            'name_lastname': forms.TextInput(attrs={'placeholder': 'Имя и фамилия'}),
            'username': forms.TextInput(attrs={'placeholder': 'Имя пользователя'}),
        }
        error_messages = {
            'email': {
                'unique': "Пользователь с такой Эл. почтой уже существует.",
            },
            'username': {
                'unique': "Пользователь с таким именем пользователя уже существует.",
            },
        }