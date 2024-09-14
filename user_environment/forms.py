# from django.core.exceptions import ValidationError
# from django.forms.utils import ErrorList
from django import forms
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
