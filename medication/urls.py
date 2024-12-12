
from django.urls import path
from . import views

app_name = 'medication'  # Define the namespace for the medication app

urlpatterns = [
    path('', views.getmedication, name="medication"),
    path('medications/', views.getMedicationReminders, name='get_medications'),  # List all reminders
    path('medications/<int:primary_key>/', views.getMedicationReminder, name='get_medication'),  # Get specific reminder by ID
    path('medications/create/', views.createMedicationReminder, name='create_medication'),  # Create a new reminder
    path('medications/<int:primary_key>/update/', views.updateMedicationReminder, name='update_medication'),  # Update existing reminder
    path('medications/<int:primary_key>/delete/', views.deleteMedicationReminder, name='delete_medication'),  # Delete reminder
    path('medications/save/', views.saveMedication, name='save_medication'),
]
