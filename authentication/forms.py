from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.forms.utils import ErrorList
from .models import User


class Registration(UserCreationForm):

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control form-control-sm'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control form-control-sm'})


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
