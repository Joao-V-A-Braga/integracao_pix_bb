from rest_framework import serializers

from ..models.PixAccount import PixAccount

class PixAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PixAccount
        exclude = ['secretId']