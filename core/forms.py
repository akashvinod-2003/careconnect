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
        # Updated fields
        fields = ['patient_name', 'service_type', 'pickup_address', 'dropoff_address', 'time_preference']
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'w-full p-4 border rounded-xl bg-gray-50', 'placeholder': 'Patient Name'}),
            'pickup_address': forms.TextInput(attrs={'class': 'w-full p-4 border rounded-xl bg-gray-50', 'placeholder': 'Home Address'}),
            'dropoff_address': forms.TextInput(attrs={'class': 'w-full p-4 border rounded-xl bg-gray-50', 'placeholder': 'Hospital/Shop Address'}),
            'service_type': forms.Select(attrs={'class': 'w-full p-4 border rounded-xl bg-white'}),
            'time_preference': forms.TextInput(attrs={'class': 'w-full p-4 border rounded-xl bg-white', 'type': 'datetime-local'}),
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