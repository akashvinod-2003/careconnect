from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ServiceRequest

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'role', 'title', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (('Role Info', {'fields': ('role', 'phone', 'title')}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Role Info', {'fields': ('role', 'phone', 'title')}),)

class RequestAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'service_type', 'status', 'pickup_lat', 'dropoff_lat']
    list_filter = ['status', 'service_type']
    search_fields = ['patient_name', 'pickup_address']
    
    # Make coordinates visible but readonly in admin for now
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Request Info', {'fields': ('family_user', 'patient_name', 'service_type', 'status', 'assigned_staff')}),
        ('Locations (Text)', {'fields': ('pickup_address', 'dropoff_address')}),
        # NEW: Section for coordinates
        ('GPS Coordinates', {'fields': (('pickup_lat', 'pickup_lng'), ('dropoff_lat', 'dropoff_lng'))}),
        ('Time', {'fields': ('time_preference', 'created_at', 'updated_at')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(ServiceRequest, RequestAdmin)