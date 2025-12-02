from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ServiceRequest

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = [
            'patient_name', 'service_type', 'time_preference',
            'pickup_address', 'dropoff_address',
            'pickup_lat', 'pickup_lng', 'dropoff_lat', 'dropoff_lng'
        ]
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'w-full p-4 border rounded-xl bg-gray-50', 'placeholder': 'Patient Name'}),
            'pickup_address': forms.TextInput(attrs={'class': 'w-full p-4 border rounded-xl bg-gray-50', 'placeholder': 'Drag Green Marker', 'readonly': 'readonly'}),
            'dropoff_address': forms.TextInput(attrs={'class': 'w-full p-4 border rounded-xl bg-gray-50', 'placeholder': 'Drag Red Marker', 'readonly': 'readonly'}),
            'service_type': forms.Select(attrs={'class': 'w-full p-4 border rounded-xl bg-white'}),
            'time_preference': forms.TextInput(attrs={'class': 'w-full p-4 border rounded-xl bg-white', 'type': 'datetime-local'}),
            
            # Hidden fields for the Map Coordinates
            'pickup_lat': forms.HiddenInput(),
            'pickup_lng': forms.HiddenInput(),
            'dropoff_lat': forms.HiddenInput(),
            'dropoff_lng': forms.HiddenInput(),
        }

class DispatchUpdateForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['status', 'assigned_staff', 'time_preference']
        widgets = {
            'status': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'assigned_staff': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'time_preference': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_staff'].queryset = User.objects.filter(role='staff')