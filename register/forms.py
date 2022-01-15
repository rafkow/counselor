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
        exclude = ['date_created', 'result', 'companies']

        widgets = {
            'signature': TextInput(attrs={'class': 'form-control'}),
            'costs': NumberInput(attrs={'class': 'form-control'}),
            'type': Select(attrs={'class': 'form-control'}),
            'bailiff': Select(attrs={'class': 'form-control'}),
            'persons': SelectMultiple(attrs={'class': 'form-control'}),
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


class RefundCreateForm(forms.ModelForm):
    class Meta:
        model = Refund
        fields = '__all__'
        widgets = {
            'create_date': TextInput(attrs={'class': 'form-control'}),
            'court_costs': NumberInput(attrs={'class': 'form-control'}),            'court_costs': NumberInput(attrs={'class': 'form-control'}),
            'clause_costs': NumberInput(attrs={'class': 'form-control'}),
            'interest': NumberInput(attrs={'class': 'form-control'}),
            'attorney_representation_costs': NumberInput(attrs={'class': 'form-control'}),
            'case': Select(attrs={'class': 'form-control'}),

        }



