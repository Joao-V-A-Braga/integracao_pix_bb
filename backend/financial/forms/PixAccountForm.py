from django import forms

from ..models.PixAccount import PixAccount

class PixAccountForm(forms.ModelForm):
    class Meta:
        model = PixAccount
        fields = ('bankAccount', 'key', 'clientId', 'secretId', 'expire_time')