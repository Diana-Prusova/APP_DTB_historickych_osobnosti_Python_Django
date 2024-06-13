"""
Modul s formuláři určenými pro správu celé databáze bojovnic
(modely jsou definované v bojovnice_app.models).
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
import re

from bojovnice_app import models


class StatyAdminForm(forms.ModelForm):
    class Meta:
        model = models.Staty
        fields = '__all__'
        labels = {
            'nazev': 'Název státu',
        }
        widgets = {
            'nazev': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dnešní název státu...'
                }),
         }

    def clean(self):
        """ Funkce pro validaci formuláře upravena tak, aby kontrolovala duplicitu."""
        print('! Spouštím StatyAdminForm - clean()')
        cleaned_data = super().clean()
        nazev = cleaned_data.get('nazev')

        if models.Staty.objects.filter(nazev__iexact=nazev).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Tento stát již existuje.')
        
        return cleaned_data


class StoletiAdminForm(forms.ModelForm):
    class Meta:
        model = models.Stoleti
        fields = '__all__'
        labels = {
            'nazev': 'Název století'
        }
        widgets = {
            'nazev': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Název století ve formátu: 1. století př. n. l. / 5. století n. l.'
                }),
        }
        help_texts = {
            'nazev': 'POZOR! Záznamy v tétto tabulce by měli být kompletní, ujistěte se, že chcete data opravdu zadat.'
        }

    def clean(self):
        """
        Funkce pro validaci formuláře upravena tak, aby kontrolovala duplicitu
        a správný formát názvu.
        """
        print('! Spouštím StoletiAdminForm - clean()')
        cleaned_data = super().clean()
        pattern = r'^([1-9]|1[0-9]|2[0-9])\. století př\. n\. l\.$|^([1-9]|1[0-9]|20)\. století n\. l\.$'
        nazev = cleaned_data.get('nazev')

        if  not re.fullmatch(pattern, nazev):
            raise forms.ValidationError('Nesprávný formát názvu století.')

        if models.Stoleti.objects.filter(nazev__iexact=nazev).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Toto století již existuje.')
        
        return cleaned_data


class BojovniceAdminForm(forms.ModelForm):
    class Meta:
        model = models.Bojovnice
        fields = '__all__'
        labels = {
            'jmeno': 'JMÉNO BOJOVNICE',
            'obdobi': 'OBDOBÍ',
            'uzemi': 'ÚZEMÍ',
            'popis': 'PODNÁZEV',
            'pribeh': 'PŘÍBĚH',
            'stat': 'STÁTY',
            'stoleti': 'STALETÍ',
        }

        widgets = {
            'jmeno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hlavní jméno bojovnice.'
                }),
            'obdobi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Roky od-do nebo století. Příklad: 1423 - 1470 / 12. století n. l. / 5. století n. l. - 6. století n. l.'
                }),
            'uzemi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Název historického území, odkud bojovnice pocházela.'
                }),
            'popis': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 1,
                'placeholder': 'Podnázev - krátký popisný text o pár slovech (max 100 znaků).'
                }),
            'pribeh': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Podrobný popis života bojovnice (max 2000 znaků).'
                }),
            'stat': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'placeholder': 'Dnešní státy, které odpovídají historickému území.'
                }),
            'stoleti': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'placeholder': 'Století, ve kterém/kterých bojovnice žila.'
                }),
        }

    def clean(self):
        """ Funkce pro validaci formuláře upravena tak, aby kontrolovala duplicitu."""
        print('! Spouštím BojovniceAdminForm - clean()')
        cleaned_data = super().clean()
        jmeno = cleaned_data.get('jmeno')
        uzemi = cleaned_data.get('uzemi')

        if models.Bojovnice.objects.filter(jmeno__iexact=jmeno, uzemi=uzemi).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Tato bojovnice již existuje.')
        
        return cleaned_data


class VsechnaJmenaAdminForm(forms.ModelForm):
    class Meta:
        model = models.VsechnaJmena
        fields = 'jmeno', 'bojovnice'
        labesl = {
            'jmeno': 'Jméno',
            'bojovnice': 'Bojovnice',
        }
        widgets = {
            'jmeno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Přidávané jméno bojovnice.'
                }),
            'bojovnice': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Vyberte bojovnici, které jméno patří.'
                }),
        }
        help_texts = {
            'jmeno': 'POZOR! Nezadávejte hlavní jméno bojovnice. To bylo přidáno automaticky.'
        
        }

        def clean(self):
            """ Funkce pro validaci formuláře upravena tak, aby kontrolovala duplicitu."""
            print('! Spouštím VsechnaJmenaAdminForm - clean()')
            cleaned_data = super().clean()
            jmeno = cleaned_data.get('jmeno')

            if models.VsechnaJmena.objects.filter(jmeno__iexact=jmeno).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Toto jméno již existuje.')
            
            return cleaned_data


class SkupinyBojovnicAdminForm(forms.ModelForm):
    class Meta:
        model = models.SkupinyBojovnic
        fields = '__all__'
        labels = {
            'jmeno': 'Název',
            'popis': 'Popis',
            'stat': 'Státy z dnešního pohledu',
            'stoleti': 'Století',
            'bojovnice': 'Přiřadit bojovnice',
        }
        widgets = {
            'jmeno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Název skupiny bojovnic.'
                }),
            'popis': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Popis skupiny bojovnic. Maximálně 5000 znaků (max 5000 znaků).'
                }),
            'stat': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'placeholder': 'Dnešní státy, které jsou spojeny s touto skupinou bojovnic.'
                }),
            'stoleti': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'placeholder': 'Století, ve kterých bojovnice žily.'
                }),
            'bojovnice': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'placeholder': 'Vyberte bojovnice, které patří do této skupiny.'
                }),
            }
        
    def clean(self):
        """Funkce pro validaci formuláře upravena tak, aby kontrolovala duplicitu."""
        print('! Spouštím SkupinyBojovnicAdminForm - clean()')
        cleaned_data = super().clean()
        jmeno = cleaned_data.get('jmeno')
        stat = cleaned_data.get('stat')
        stoleti = cleaned_data.get('stoleti')

        if models.SkupinyBojovnic.objects.filter(jmeno__iexact=jmeno).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Tato skupina bojovnic již existuje.')
        
        return cleaned_data
        

class MyAuthenticationForm(AuthenticationForm):
    """ Přizpůsobení formuláře pro přihlášení."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.widgets.TextInput(attrs={
                'class': 'form-control'
            })
        self.fields['password'].widget = forms.widgets.PasswordInput(attrs={
                'class': 'form-control'
            })