from django import forms

from ..models.Bank import Bank


class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ('name', 'code')