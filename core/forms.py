from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ServiceRequest

# 1. Signup Form
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        # We don't show 'role' here so they default to 'Family' automatically
        fields = ['username', 'email', 'first_name', 'last_name']

# 2. Family Booking Form
class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['patient_name', 'service_type', 'location', 'time_preference']
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'w-full p-4 border rounded-xl bg-gray-50', 'placeholder': 'Patient Name'}),
            'location': forms.TextInput(attrs={'class': 'w-full p-4 border rounded-xl bg-gray-50', 'placeholder': 'Pickup Address'}),
            'service_type': forms.Select(attrs={'class': 'w-full p-4 border rounded-xl bg-white'}),
            'time_preference': forms.Select(choices=[('ASAP', 'ASAP'), ('1 Hour', 'In 1 Hour'), ('Tomorrow', 'Tomorrow')], attrs={'class': 'w-full p-4 border rounded-xl bg-white'}),
        }

# 3. Dispatch Form
class DispatchUpdateForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['status', 'assigned_staff']
        widgets = {
            'status': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'assigned_staff': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show users with 'staff' role in the dropdown
        self.fields['assigned_staff'].queryset = User.objects.filter(role='staff')