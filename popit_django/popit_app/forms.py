from django import forms
from .models import *


class inscription_form(forms.Form):
    prenom = forms.CharField(label_suffix = " : ", label = 'Prénom', max_length=255, widget=forms.TextInput({'class':'form-control'}))
    nom = forms.CharField(label_suffix = " : ", label = 'Nom', max_length=255, widget=forms.TextInput({'class':'form-control'}))
    email = forms.EmailField(label_suffix = " : ", label = 'Adresse mail', widget=forms.EmailInput({'placeholder': 'Entrez votre adresse mail', 'class':'form-control'}))
    pseudo = forms.CharField(label_suffix = " : ", label = 'Pseudo', max_length=255, widget=forms.TextInput({'class':'form-control'}))
    pays = forms.ChoiceField(label_suffix = " : ", label = 'Pays', choices = [('Belgique', 'Belgique'), ('France','France'), ('Luxembourg','Luxembourg'), ('Pays-Bas', 'Pays-Bas')], widget=forms.Select({'class':'form-control'}))
    password = forms.CharField(label_suffix = " : ", label = 'Mot de passe',max_length=30, widget=forms.PasswordInput({'class':'form-control'}))
    password2 = forms.CharField(label_suffix = " : ", label = 'Confirmation du mot de passe',max_length=30, widget=forms.PasswordInput({'class':'form-control'}))
    

class connexion_form(forms.Form):
    email = forms.EmailField(label_suffix = " : ", label = 'Adresse mail', widget=forms.EmailInput({'placeholder': 'Entrez votre adresse mail', 'class':'form-control', 'name': 'email'}))
    password = forms.CharField(label_suffix = " : ", label = 'Mot de passe',max_length=30, widget=forms.PasswordInput({'class':'form-control'}))

