from django.forms import Textarea, TextInput, SelectMultiple, Select, NumberInput
from django import forms
from .models import *


class PersonCreateFrom(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ['date_created']

        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'pesel': TextInput(attrs={'class': 'form-control'}),
            'address': TextInput(attrs={'class': 'form-control'}),
            'phone': TextInput(attrs={'class': 'form-control'}),
            'note': Textarea(attrs={'class': 'form-control'}),
        }


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        exclude = ['date_created', 'result', 'companies', 'accused_companies', 'prosecutor_persons',
                   'prosecutor_companies', 'bailiff', 'costs', 'accused_persons']

        widgets = {
            'signature': TextInput(attrs={'class': 'form-control'}),
            'type': Select(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
        }


class CaseEditForm(forms.ModelForm):
    class Meta:
        model = Case
        exclude = ['date_created', 'result', 'companies',
                   'accused_persons', 'accused_companies', 'prosecutor_persons', 'prosecutor_companies']

        widgets = {
            'signature': TextInput(attrs={'class': 'form-control'}),
            'costs': NumberInput(attrs={'class': 'form-control'}),
            'type': Select(attrs={'class': 'form-control'}),
            'bailiff': Select(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
        }


class FamilyCreateForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'persons': SelectMultiple(attrs={'class': 'form-control'}),
        }


class BailiffCreateForm(forms.ModelForm):
    class Meta:
        model = Bailiff
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
        }


class ImportDataForm(forms.Form):
    data = forms.CharField(widget=Textarea(attrs={"rows": 20, 'class': 'form-control'}))


class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'nip']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'nip': NumberInput(attrs={'class': 'form-control'}),
        }


