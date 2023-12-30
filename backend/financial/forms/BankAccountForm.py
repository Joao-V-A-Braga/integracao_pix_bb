from django import forms

from ..models.BankAccount import BankAccount


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ('number', 'agency', 'cnpj', 'bank')