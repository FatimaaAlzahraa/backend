from rest_framework import serializers
from .models import MedicationManagement

class MedicationManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationManagement
        fields = '__all__'  # This includes all fields from the model