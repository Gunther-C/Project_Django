from django import forms
from django.forms.utils import ErrorList
from .models import User


class Registration(forms.ModelForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'Votre nom d\'utilisateur'}),
        label='', help_text=''
    )

    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'Votre E-mail'}), label='')

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'Votre Mot de passe'}), label='')

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'Confirmez Votre mot de passe'}), label='')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def add_error_to_all(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, ErrorList())
        errors.append(message)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if len(password1) < 8:
            self.add_error_to_all("Le mot de passe doit comporter minimum huit caractères.")

        if password1 and password2 and password1 != password2:
            self.add_error_to_all("Les mots de passe ne correspondent pas.")

        # return cleaned_data


class Connection(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control form-control-sm', 'placeholder': 'Votre E-mail'}
        ),
        label=''
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-sm', 'placeholder': 'Votre Mot de passe'}
        ),
        label=''
    )
