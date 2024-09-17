# from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import Ticket, Review


class NewTicket(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}), label='Titre')
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '6', 'maxlength': '2000'}),
        label='Votre demande'
    )
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control form-control-sm w-50'}),
                             required=False)

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class NewReview(forms.ModelForm):

    title_review = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}), label='Titre')

    CHOICES = [(1, '1-'), (2, '2-'), (3, '3-'), (4, '4-'), (5, '5-')]
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label='Note')

    details = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '6', 'maxlength': '8150'}),
                              label='Commentaire', required=False)

    class Meta:
        model = Review
        fields = ['title_review', 'rating', 'details']


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
