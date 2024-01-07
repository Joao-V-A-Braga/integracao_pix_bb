from rest_framework import serializers

from ..models.ParcelPix import ParcelPix

class ParcelPixSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParcelPix
        fields = '__all__'