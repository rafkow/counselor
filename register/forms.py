from django.forms import Textarea, TextInput, SelectMultiple, Select, NumberInput
from django import forms
from .models import *


class PersonCreateFrom(forms.ModelForm):
    class Meta:
        model = Person
        # exclude = ['date_created']
        fields = '__all__'

        widgets = {
            # 'id': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'pesel': TextInput(attrs={'class': 'form-control'}),
            'address': TextInput(attrs={'class': 'form-control'}),
            'phone': TextInput(attrs={'class': 'form-control'}),
            'street': TextInput(attrs={'class': 'form-control'}),
            'city': TextInput(attrs={'class': 'form-control'}),
            'postcode': TextInput(attrs={'class': 'form-control'}),
            'note': Textarea(attrs={'class': 'form-control'}),
        }


class PersonUpdateForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        # exclude = ['date_created', 'result', 'companies', 'accused_companies', 'prosecutor_persons',
        #            'prosecutor_companies', 'bailiff', 'costs', 'accused_persons']
        fields = ['signature', 'type', 'accused_persons', 'description', ]

        widgets = {
            'signature': TextInput(attrs={'class': 'form-control'}),
            'type': Select(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'accused_persons': SelectMultiple(attrs={'class': 'form-control'})
        }


class SimpleCaseCreateForm(forms.Form):
    signature = forms.CharField(label='sygnatura', max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = forms.ChoiceField(label='typ sprawy', choices=Case.TYPE,
                             widget=forms.Select(attrs={'class': 'form-control'}))


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


class CaseCourtReferenceForm(forms.Form):
    pk = forms.IntegerField(widget=forms.HiddenInput)
    court_reference_number = forms.CharField(
        label="Przypisz sygnaturę sądową",
        widget=TextInput(attrs={'class': 'form-control'})
    )


class CaseAssignBailiffForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['id', 'bailiff']

        widgets = {
            'bailiff': Select(attrs={'class': 'form-control'})
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
            'office_name': TextInput(attrs={'class': 'form-control'}),
            'street': TextInput(attrs={'class': 'form-control'}),
            'city': TextInput(attrs={'class': 'form-control'}),
            'postcode': TextInput(attrs={'class': 'form-control'})}


class ImportDataForm(forms.Form):
    data = forms.CharField(widget=Textarea(attrs={"rows": 20, 'class': 'form-control'}))


class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'nip', 'krs']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'krs': TextInput(attrs={'class': 'form-control'}),
            'nip': NumberInput(attrs={'class': 'form-control'}),
        }


