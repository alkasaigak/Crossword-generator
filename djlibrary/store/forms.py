from django import forms
from django.forms import (formset_factory, modelformset_factory)

from .models import (Book, Author)


class BookForm(forms.Form):
    name = forms.CharField(
        label='Слово',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите слово сюда'
        })
    )


BookFormset = formset_factory(BookForm)
