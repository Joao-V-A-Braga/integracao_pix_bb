from rest_framework import serializers

from ..models.Bank import Bank


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'