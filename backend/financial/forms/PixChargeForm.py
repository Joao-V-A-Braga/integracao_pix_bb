from django import forms

from ..models.PixCharge import PixCharge

class PixChargeForm(forms.ModelForm):
    class Meta:
        model = PixCharge
        fields = (
            "pixAccount", "key", "value", "status", "expiration", "code",
            "txid", "location", "e2eid"
            )