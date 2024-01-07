from rest_framework import serializers

from ..models.PixCharge import PixCharge

class PixChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PixCharge
        fields = '__all__'