"""
Formuláře pro vyhledávání v databázi na uživetelské indexové stránce.

Vyhledávání je možné podle státu, století a jména bojovnice a každý formulář
vyhledává data jak v tabulce Bojovnice, tak i v tabulce SkupinyBojovnic.

Formuláře pracují samostatně, lze vyhledávat pouze podle jednoho kritéria.
"""

from django import forms
from bojovnice_app import models


class SearchByStatForm(forms.Form):
    stat = forms.ModelChoiceField(
        queryset=models.Staty.objects.all(),
        label='VYHLEDAT PODLE STÁTU',
        empty_label='Vyberte stát...',
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class SearchByStoletiForm(forms.Form):
    stoleti = forms.ModelChoiceField(
        queryset=models.Stoleti.objects.all(),
        label='VYHLEDAT PODLE STOLETÍ',
        empty_label='Vyberte století...',
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class SeachByVsechnaJmenaForm(forms.Form):
    jmeno = forms.CharField(
        label='VYHLEDAT PODLE JMÉNA',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Zadejte jméno nebo jeho čast...'
        })
    )

