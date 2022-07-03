from django.forms import TextInput, Select, NumberInput, HiddenInput
from django import forms
from payments.models import Refund, Payments


class RefundCreateForm(forms.ModelForm):
    class Meta:
        model = Refund
        fields = '__all__'
        widgets = {
            'create_date': TextInput(attrs={'class': 'form-control'}),
            'court_costs': NumberInput(attrs={'class': 'form-control'}),
            'clause_costs': NumberInput(attrs={'class': 'form-control'}),
            'interest': NumberInput(attrs={'class': 'form-control'}),
            'attorney_representation_costs': NumberInput(attrs={'class': 'form-control'}),
            'case': Select(attrs={'class': 'form-control'}),
        }


class PaymentCreateForm(forms.ModelForm):
    class Meta:
        model = Payments
        fields = '__all__'
        widgets = {
            'create_date': TextInput(attrs={'class': 'form-control'}),
            'value': NumberInput(attrs={'class': 'form-control'}),
            'refund': HiddenInput(attrs={'class': 'form-control'}),
        }


