from django import forms
from .models import MedicationManagement

class MedicationForm(forms.ModelForm):
    class Meta:
        model = MedicationManagement
        fields = ['medicine_name', 'route_of_administration', 'dosage_unit_of_measure',
                  'dosage_quantity_of_units_per_time', 'periodic_interval', 'dosage_frequency', 'first_time_of_intake']
