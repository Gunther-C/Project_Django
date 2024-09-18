from django import forms
from django.contrib.auth.forms import PasswordChangeForm
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
        ), required=True, label=''
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-sm', 'placeholder': 'Votre Mot de passe'}
        ), required=True, label=''
    )


class NewPassword(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control form-control-sm'})

        """self.fields['new_password1'].help_text = None
        self.fields['new_password2'].help_text = None"""

    def add_error_to_all(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, ErrorList())
        errors.append(message)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if len(password1) < 8:
            self.add_error_to_all("Le mot de passe doit comporter minimum huit caractères.")

        if password1 and password2 and password1 != password2:
            self.add_error_to_all("Les mots de passe ne correspondent pas.")


class NewEmail(forms.Form):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm'}),
        required=True, label='Votre Mot de passe'
    )

    new_mail1 = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-sm'}),
        required=True, label='Votre E-mail'
    )

    new_mail2 = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-sm'}),
        required=True, label='Confirmez la nouvelle adresse e-mail'
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(NewEmail, self).__init__(*args, **kwargs)

    def add_error_to_all(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, ErrorList())
        errors.append(message)

    def clean_password(self):
        _password = self.cleaned_data["password"]
        if not self.user.check_password(_password):
            self.add_error_to_all("Mot de passe incorrect.")
        return _password

    def clean_new_mail2(self):
        mail1 = self.cleaned_data.get("new_mail1")
        mail2 = self.cleaned_data.get("new_mail2")
        if mail1 and mail2 and mail1 != mail2:
            self.add_error_to_all("Les deux adresses e-mail ne correspondent pas.")
        return mail2

    """def save(self, commit=True):
        self.user.email = self.cleaned_data["new_email1"]
        if commit:
            self.user.save()
        return self.user"""
