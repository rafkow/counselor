from django.forms import Textarea, TextInput, SelectMultiple, Select, NumberInput
from django import forms
from .models import Person, Case, Family


class PersonCreateFrom(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ['date_created']


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        exclude = ['date_created', 'result']

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


class ImportDataForm(forms.Form):
    data = forms.CharField(widget=Textarea(attrs={"rows": 20, 'class': 'form-control'}))


