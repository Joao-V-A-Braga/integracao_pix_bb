from rest_framework import serializers

from ..models.InvoiceToReceive import InvoiceToReceive

class InvoiceToReceiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceToReceive
        fields = '__all__'