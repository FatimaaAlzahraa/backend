#backend/medication/view.py
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import MedicationManagement
from .medication_management_serializers import MedicationManagementSerializer
from rest_framework.permissions import IsAuthenticated
import json
import requests
import logging
import requests

# Helper function to fetch drug interaction severity from Flask API
def fetch_drug_interaction(medicine_name, drug_name):
    url = 'http://127.0.0.1:5001/input'  # Flask API endpoint
    try:
        response = requests.post(url, json={'drug_a': medicine_name, 'drug_b': drug_name})
        if response.status_code == 200:
            data = response.json()
            return data.get('severity', 'No severity message available')
        else:
            return 'Error fetching drug interaction'
    except requests.exceptions.RequestException as e:
        return str(e)



# 1. Get Routes for API Documentation (List all available routes)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])  # Optional if you want to restrict to authenticated users
def getmedication(request):
    routes = [
        {
            'Endpoint': '/medication/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of medication'
        },
        {
            'Endpoint': '/medication/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single medication object'
        },
        {
            'Endpoint': '/medication/create/',
            'method': 'POST',
            'body': None ,
            # 'body': {'body': ""},
            'description': 'Creates new medication with data sent in post request'
        },
        {
            'Endpoint': '/medication/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing medication with data sent in post request'
        },
        {
            'Endpoint': '/medication/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes an existing medication'
        },
    ]
    return Response(routes)


# 2. List all medication reminders for the authenticated user
@api_view(['GET'])
# @permission_classes([IsAuthenticated])  # Only authenticated users can access
def getMedicationReminders(request):
    reminders = MedicationManagement.objects.all()
    # reminders = MedicationManagement.objects.filter(user=request.user)
    serializer = MedicationManagementSerializer(reminders, many=True)
    return Response(serializer.data)


# 3. Get a specific medication reminder by ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMedicationReminder(request, primary_key):
    try:
        reminder = MedicationManagement.objects.get(id=primary_key, user=request.user)
    except MedicationManagement.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=404)
    
    serializer = MedicationManagementSerializer(reminder)
    return Response(serializer.data)


# 4. Create a new medication reminder
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Only authenticated users can access
#     data = json.loads(request.data)  # Get form data from the request
def createMedicationReminder(request):
    data = request.data  # Use the parsed request data

    # Validate required fields
    required_fields = ['medicine_name', 'route_of_administration', 'dosage_unit_of_measure',
                       'dosage_quantity_of_units_per_time', 'periodic_interval',
                       'dosage_frequency', 'first_time_of_intake']
    for field in required_fields:
        if field not in data:
            return Response({'detail': f'Missing field: {field}'}, status=400)

    # Create a medication reminder
    user = request.user if request.user.is_authenticated else None
    reminder = MedicationManagement.objects.create(
        user=request.user,
        medicine_name=data['medicine_name'],
        route_of_administration=data['route_of_administration'],
        dosage_unit_of_measure=data['dosage_unit_of_measure'],
        dosage_quantity_of_units_per_time=data['dosage_quantity_of_units_per_time'],
        periodic_interval=data['periodic_interval'],
        dosage_frequency=data['dosage_frequency'],
        first_time_of_intake=data['first_time_of_intake'],
        stopped_by_datetime=data.get('stopped_by_datetime')
    )

    # Fetch interaction severity from Flask API
    severity = fetch_drug_interaction(data['medicine_name'], data['medicine_name'])
    reminder.drug_interaction_severity = severity
    reminder.save()

    # Serialize the response
    serializer = MedicationManagementSerializer(reminder, many=False)
    return Response(serializer.data)


# 5. Update an existing medication reminder
@api_view(['PUT'])
# @permission_classes([IsAuthenticated])
def updateMedicationReminder(request, primary_key):
    try:
        reminder = MedicationManagement.objects.get(id=primary_key, user=request.user)
    except MedicationManagement.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=404)

    # Update medication fields from the request data
    serializer = MedicationManagementSerializer(reminder, data=request.data)
    if serializer.is_valid():
        serializer.save()  # Save the updated medication record
        
        # Fetch the updated drug interaction severity from Flask API
        severity = fetch_drug_interaction(reminder.medicine_name, reminder.medicine_name)
        
        # Update the interaction severity field
        reminder.drug_interaction_severity = severity
        reminder.save()

        return Response(serializer.data)
    
    return Response(serializer.errors, status=400)


# 6. Delete a medication reminder by ID
@api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
def deleteMedicationReminder(request, primary_key):
    try:
        reminder = MedicationManagement.objects.get(id=primary_key, user=request.user)
    except MedicationManagement.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=404)

    reminder.delete()  # Delete the medication reminder from the database
    return Response({'detail': 'Deleted successfully.'}, status=204)  # No content response


# 7. Save a new medication entry (alternative way to save medication)
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def saveMedication(request):
    data = request.data
    serializer = MedicationManagementSerializer(data=data)
    if serializer.is_valid():
        # Save medication with the current user
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
# Create your views here.
