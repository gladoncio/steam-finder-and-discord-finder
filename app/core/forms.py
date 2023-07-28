from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import ModelForm, fields, Form
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

class SteamSearchForm(forms.Form):
    buscador = forms.CharField(widget=forms.TextInput(
    attrs={'class':'form-control col-md-12','type':'text', 'name': 'buscador','placeholder':'Buscador'}),
    label='')
    class Meta:
        fields = ['buscador',]