from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ServiceRequest

# SignUp Form for New Users
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Last Name'}),
        }

# Form for Family members to book a ride
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

# Form for Admins to update status/assign staff
class DispatchUpdateForm(forms.ModelForm):
    assigned_staff = forms.ModelChoiceField(
        queryset=User.objects.filter(role='staff'),
        required=False,
        widget=forms.Select(attrs={'class': 'w-full p-2 border rounded'})
    )

    class Meta:
        model = ServiceRequest
        fields = ['status', 'assigned_staff']
        widgets = {
            'status': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
        }