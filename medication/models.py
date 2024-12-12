from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class MedicationManagement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=100)
    route_of_administration = models.CharField(
    null=True, 
    blank=False, 
    choices=(
        ('oral', 'Orally'),  #The medication is taken orally 
        ('parentral/im', 'Intra-muscular'), #The medication is given intra-muscularly 
        ('parentral/iv', 'Intravenous'), #The medication is given intravenously 
    ), 
    max_length=256
)
    dosage_unit_of_measure = models.CharField(
    null=True, 
    blank=False, 
    choices=(
        ('tablet', 'Tablet'), #measured in tablets (2 tablets).
        ('capsule', 'Capsule'),  #measured in capsules
        ('gravimetric/mg', 'Milligram/mg'), #measured in milligrams (50 mg).
        ('volumetric/ml', 'Milliliter/ml'), #measured in milliliters (5 ml of syrup).
    ), 
    max_length=256
)
    #This field stores the quantity of the dosage unit that should be taken at a specific time.
    dosage_quantity_of_units_per_time = models.FloatField(null=True, blank=False)
    dosage_frequency = models.PositiveIntegerField(null=True, blank=False)
    #This field specifies how often the medication or regimen is to be taken (i.e., the periodic interval).
    periodic_interval = models.CharField(
    null=True, 
    blank=False, 
    choices=(
        ('daily', 'Daily Regimen'),
        ('weekly', 'Weekly Regimen'),
        ('monthly', 'Monthly Regimen'),
    ), 
    max_length=256
)
    first_time_of_intake = models.DateTimeField(null=True, blank=False, default=timezone.now)
    stopped_by_datetime = models.DateTimeField(null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True) # automatically fetch the time and date of the moment on each sql update
    create_date = models.DateTimeField(auto_now_add=True) # automatically fetch the time and date of the moment only at the time of creation (sql insertion)
    drug_interaction_severity = models.TextField(null=True, blank=True)
    

    def __str__(self):
        return f"Medication Record for {self.user.username} - {self.medication_name}"
