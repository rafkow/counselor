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

    # def __init__(self, data, **kwargs):
    #     initial = kwargs.get('initial', {})
    #     data = {**initial, **data}
    #     super().__init__(data, **kwargs)


class FamilyCreateForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'persons': SelectMultiple(attrs={'class': 'form-control'}),
        }



