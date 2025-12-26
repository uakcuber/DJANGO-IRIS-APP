# iris_app/serializers.py
from rest_framework import serializers
from .models import IrisPlant

class IrisPlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = IrisPlant
        fields = '__all__'  # Tüm alanları API'de göster