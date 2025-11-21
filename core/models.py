from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Custom User Model (Handles Roles)
class User(AbstractUser):
    ROLE_CHOICES = (
        ('family', 'Family Member'),
        ('staff', 'Staff (Driver/Nurse)'),
        ('admin', 'Dispatcher (Admin)'),
        ('manager', 'Manager (Owner)'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='family')
    phone = models.CharField(max_length=15, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. Senior Nurse")

    def __str__(self):
        return f"{self.username} ({self.role})"

# 2. Service Request Model
class ServiceRequest(models.Model):
    SERVICE_TYPES = (
        ('Hospital Visit', 'Hospital Visit'),
        ('Medicine Pickup', 'Medicine Pickup'),
        ('Home Help', 'Home Help'),
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    )

    # Who asked for help?
    family_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests_created')
    
    # Who is doing the job? (Nullable until assigned)
    assigned_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='requests_assigned')
    
    # Details
    patient_name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    location = models.CharField(max_length=200)
    time_preference = models.CharField(max_length=50, default="ASAP")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient_name} - {self.service_type}"