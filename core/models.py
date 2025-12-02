from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('family', 'Family Member'),
        ('staff', 'Staff (Driver/Nurse)'),
        ('admin', 'Dispatcher (Admin)'),
        ('manager', 'Manager (Owner)'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='family')
    phone = models.CharField(max_length=15, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

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
        ('Declined', 'Declined'),
    )

    family_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests_created')
    assigned_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='requests_assigned')
    
    patient_name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    
    # Addresses (Text)
    pickup_address = models.CharField(max_length=255, default="", blank=True)
    dropoff_address = models.CharField(max_length=255, default="", blank=True)
    
    # Coordinates (Numbers for the Map)
    pickup_lat = models.FloatField(null=True, blank=True)
    pickup_lng = models.FloatField(null=True, blank=True)
    dropoff_lat = models.FloatField(null=True, blank=True)
    dropoff_lng = models.FloatField(null=True, blank=True)
    
    time_preference = models.CharField(max_length=100, default="ASAP") 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient_name} - {self.service_type}"